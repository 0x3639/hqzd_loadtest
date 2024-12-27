# Quick Start: Load Testing

## Step 1: Clone from GitHub
1. Clone this repository from GitHub:
   ```bash
   git clone https://github.com/0x3639/hqzd_loadtest.git
   cd hqzd_loadtest
   ```

## Step 2: Rename and Configure .env
1. Rename the example environment file:
   ```bash
   mv .env.example .env
   ```
2. Open the “.env” file and edit the variables as needed:
   - URL: Node endpoint for sending/receiving (“http://127.0.0.1:35997” by default).  
   - PASSWORD: Wallet password used by nomctl.  
   - ADDRESSES: A JSON array of addresses like '["z1qabc...", "z1qxyz..."]'.

## Step 3: Create and Activate a Virtual Environment
1. Create and activate a virtual environment (required for isolation):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

## Step 4: Run the Load Test Interactively
Invoke the main script, specifying intervals and workers:

```bash
python run_loadtest.py --receive-interval 60 --send-workers 1 --send-interval 5
```
- --receive-interval: seconds between receiveAll calls (default: 60).  
- --send-workers: number of concurrent threads sending transactions (default: 1).  
- --send-interval: delay (seconds) each thread waits between sends (default: 5).

Press Ctrl + C at any time to stop the load test.

## (Optional) Running via nohup
If you’d like this to continue running after closing your terminal, use nohup:

```bash
nohup python run_loadtest.py --receive-interval 60 --send-workers 1 --send-interval 5 > loadtest.log 2>&1 &
```
Then:  
- Use “tail -f loadtest.log” to monitor logs in real time.  
- Stop the background process by using “pkill python” or a similar mechanism.

## Stopping the Load Test (If nohup Used)
To find and terminate the running load test, you can:
```bash
ps aux | grep run_loadtest
kill -9 <PID_OF_run_loadtest>
```
or simply:
```bash
pkill -f run_loadtest.py
```
Choose whichever method you prefer to ensure the process is completely stopped.
