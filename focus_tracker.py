#!/usr/bin/env python3
# focus_tracker.py

import argparse
import csv
import os
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.focus_log.csv")

def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Start Time", "End Time", "Duration (minutes)"])

def parse_args():
    parser = argparse.ArgumentParser(description='Track focused work time')
    parser.add_argument('command', choices=['start', 'stop', 'report', 'status'], 
                        help='start: Start a new session\nstop: End current session\nreport: Show summary\nstatus: Check current session')
    return parser.parse_args()

def get_current_session():
    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        rows = list(reader)
        if rows and len(rows[-1]) < 3:  # If last row has no end time
            return rows[-1][0]
    return None

def start_session():
    current = get_current_session()
    if current:
        print(f"Already have an active session since {current}. Stop it first.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([now])
    print(f"Started focus session at {now}")

def end_session():
    current = get_current_session()
    if not current:
        print("No active session to stop")
        return

    now = datetime.now()
    with open(LOG_FILE, 'r') as f:
        lines = list(csv.reader(f))
    
    # Calculate duration
    start_time = datetime.strptime(lines[-1][0], "%Y-%m-%d %H:%M")
    duration = (now - start_time).total_seconds() / 60
    
    # Update last line with end time and duration
    lines[-1].extend([now.strftime("%Y-%m-%d %H:%M"), f"{duration:.1f}"])
    
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    
    print(f"Ended session at {now.strftime('%H:%M')}. Duration: {duration:.1f} minutes")

def show_status():
    current = get_current_session()
    if current:
        print(f"Currently tracking since {current}")
        return
    print("No active session")

def generate_report():
    total = 0
    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 3:
                total += float(row[2])
    
    print(f"Total focused time: {total:.1f} minutes ({total/60:.2f} hours)")

def main():
    init_log()
    args = parse_args()
    
    try:
        if args.command == 'start':
            start_session()
        elif args.command == 'stop':
            end_session()
        elif args.command == 'status':
            show_status()
        elif args.command == 'report':
            generate_report()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()