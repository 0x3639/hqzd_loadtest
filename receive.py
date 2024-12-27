#!/usr/bin/env python3
import os
import time
import argparse
import subprocess
from dotenv import load_dotenv
import logging

# Load environment variables from .env
load_dotenv()

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    parser = argparse.ArgumentParser(description="Run receiveAll every X seconds.")
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Number of seconds between each receiveAll execution (default: 60)."
    )
    args = parser.parse_args()

    url = os.getenv("URL", "http://127.0.0.1:35997")
    password = os.getenv("PASSWORD", "Don'tTrust.Verify")

    # Adjust path to nomctl if needed (up one level to /nomctl/build/)
    nomctl_path = "../nomctl/build/nomctl"

    receive_command = [
        nomctl_path,
        "-hq", "znn-cli",
        "-u", url,
        "-k", "hqz",
        "-p", password,
        "-n", "26",
        "receiveAll"
    ]

    logging.info(f"[receive.py] Starting receive loop. Interval = {args.interval}s")

    while True:
        # Create a safe command string for logging (mask password)
        safe_command_str = ' '.join("****" if arg == password else arg for arg in receive_command)
        logging.info(f"[receive.py] Executing: {safe_command_str}")

        try:
            subprocess.run(receive_command, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"[receive.py] Error running receiveAll: {e}")

        # Sleep for the specified interval
        time.sleep(args.interval)

if __name__ == "__main__":
    main()