#!/usr/bin/env python3
import os
import time
import threading
import argparse
import subprocess
from dotenv import load_dotenv
import json
import logging

# Load environment variables from .env
load_dotenv()

def worker_thread(thread_id, interval, nomctl_path, url, password, addresses, address_locks, wallet_lock, amount):
    """
    Each worker:
      - Loops forever
      - Sends to each address in turn
      - Acquires a lock per address to avoid concurrent sends from the same address
      - Also acquires a global lock to avoid concurrent calls to nomctl
      - Sleeps 'interval' seconds after each send
    """
    send_command_base = [
        nomctl_path,
        "-hq", "znn-cli",
        "-u", url,
        "-k", "hqz",
        "-p", password,
        "send"
    ]
    
    logging.info(f"[Thread {thread_id}] Starting worker loop...")
    while True:
        for address in addresses:
            with wallet_lock:  # <--- Prevent nomctl concurrency
                with address_locks[address]:
                    cmd = send_command_base + [address, str(amount), "zts1utylzxxxxxxxxxxx6agxt0"]

                    safe_cmd_str = ' '.join("****" if arg == password else arg for arg in cmd)
                    logging.info(f"[Thread {thread_id}] Executing: {safe_cmd_str}")

                    try:
                        subprocess.run(cmd, check=True)
                    except subprocess.CalledProcessError as e:
                        logging.error(f"[Thread {thread_id}] Error running send command: {e}")
            time.sleep(interval)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    parser = argparse.ArgumentParser(description="Spin up multiple concurrent send workers (serialized per address).")
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of concurrent workers to spawn (default: 1)."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Seconds to wait between sends per worker (default: 5)."
    )
    args = parser.parse_args()
    
    # Read from .env or fallback
    url = os.getenv("URL", "http://127.0.0.1:35997")
    password = os.getenv("PASSWORD", "Don'tTrust.Verify")
    addresses_str = os.getenv("ADDRESSES", "")
    if not addresses_str.strip():
        print("[send_spam.py] No addresses found in .env. Exiting.")
        return
    
    addresses = json.loads(os.getenv("ADDRESSES", "[]"))
    
    # Read integer-based SEND_AMOUNT from .env; default to 1 if invalid or below 1
    amount_str = os.getenv("SEND_AMOUNT", "1")
    try:
        amount = int(amount_str)
        if amount < 1:
            raise ValueError("Minimum amount is 1")
    except ValueError:
        logging.warning(f"[send_spam.py] Invalid or below-minimum SEND_AMOUNT '{amount_str}', defaulting to 1")
        amount = 1

    # Read TOKEN_STANDARD from .env
    token_standard = os.getenv("TOKEN_STANDARD", "zts1utylzxxxxxxxxxxx6agxt0")

    # Path to nomctl
    nomctl_path = "../nomctl/build/nomctl"

    # Create a lock for each address
    address_locks = {addr: threading.Lock() for addr in addresses}
    wallet_lock = threading.Lock()  # <--- New global lock

    # Spawn worker threads
    threads = []
    for i in range(args.workers):
        t = threading.Thread(
            target=worker_thread,
            args=(i, args.interval, nomctl_path, url, password, addresses, address_locks, wallet_lock, amount),
            daemon=True
        )
        t.start()
        threads.append(t)

    # Keep main thread alive
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()