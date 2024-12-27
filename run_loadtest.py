#!/usr/bin/env python3
import argparse
import subprocess
import time
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    parser = argparse.ArgumentParser(
        description="Run both receive.py and send_spam.py automatically."
    )
    parser.add_argument(
        "--receive-interval",
        type=int,
        default=60,
        help="Interval for receive.py (default: 60)."
    )
    parser.add_argument(
        "--send-workers",
        type=int,
        default=1,
        help="Number of workers for send_spam.py (default: 1)."
    )
    parser.add_argument(
        "--send-interval",
        type=int,
        default=5,
        help="Interval (in seconds) between sends in send_spam.py (default: 5)."
    )
    args = parser.parse_args()

    # Start receive.py
    receive_cmd = [
        "python3",
        "receive.py",
        "--interval",
        str(args.receive_interval)
    ]
    logging.info("[run_loadtest.py] Spawning receive.py process...")
    receive_process = subprocess.Popen(receive_cmd)

    # Start send_spam.py
    send_cmd = [
        "python3",
        "send_spam.py",
        "--workers",
        str(args.send_workers),
        "--interval",
        str(args.send_interval)
    ]
    logging.info("[run_loadtest.py] Spawning send_spam.py process...")
    send_process = subprocess.Popen(send_cmd)

    try:
        # Keep this script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("[run_loadtest.py] Caught KeyboardInterrupt, shutting down...")
        # Terminate child processes
        receive_process.terminate()
        send_process.terminate()

if __name__ == "__main__":
    main()