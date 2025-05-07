#!/usr/bin/env python3
"""A command-line tool for tracking focused work time."""

import argparse
import csv
import os
from datetime import datetime
import pandas as pd

LOG_FILE = os.path.expanduser("~/.focus_log.csv")

def init_log():
    """Initialize the log file if it doesn't exist."""
    try:
        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Start Time", "End Time", "Duration (minutes)"])
    except Exception as e:
        print(f"Error initializing log file: {str(e)}")
        raise

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Track focused work time')
    parser.add_argument('command', choices=['start', 'stop', 'report', 'status', 'export'], 
                        help='start: Start a new session\nstop: End current session\nreport: Show summary\nstatus: Check current session\nexport: Export to Excel')
    parser.add_argument('--output', '-o', 
                        help='Output file for export (default: focus_tracker_export.xlsx)',
                        default='focus_tracker_export.xlsx')
    return parser.parse_args()

def get_current_session():
    """Get the current active session if any."""
    if not os.path.exists(LOG_FILE):
        return None
        
    try:
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header
            rows = list(reader)
            
        if not rows:  # No sessions yet
            return None
            
        last_row = rows[-1]
        if len(last_row) == 1:  # Only start time (active session)
            return last_row[0]
        return None  # Last session was completed
            
    except (FileNotFoundError, StopIteration, IndexError):
        return None

def start_session():
    """Start a new focus session."""
    current = get_current_session()
    if current:
        print(f"Already have an active session since {current}. Stop it first.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now])
    print(f"Started focus session at {now}")

def end_session():
    """End the current focus session."""
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
    """Show the status of the current session."""
    current = get_current_session()
    if current:
        print(f"Currently tracking since {current}")
        return
    print("No active session")

def generate_report():
    """Generate a report of total focused time."""
    total = 0
    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 3:
                total += float(row[2])
    
    print(f"Total focused time: {total:.1f} minutes ({total/60:.2f} hours)")

def export_to_excel(output_file):
    """Export focus tracking data to Excel with formatting."""
    try:
        # Read CSV into pandas DataFrame
        df = pd.read_csv(LOG_FILE)
        
        # Convert time columns to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M')
        df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M')
        
        # Add some summary statistics
        total_duration = df['Duration (minutes)'].sum()
        total_sessions = len(df)
        avg_duration = df['Duration (minutes)'].mean()
        
        # Create Excel writer object
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Write main data
            df.to_excel(writer, sheet_name='Sessions', index=False)
            
            # Create summary sheet
            summary_data = {
                'Metric': ['Total Sessions', 'Total Duration (minutes)', 'Total Duration (hours)', 'Average Session (minutes)'],
                'Value': [total_sessions, total_duration, total_duration/60, avg_duration]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Get workbook and worksheet objects for formatting
            workbook = writer.book
            sessions_sheet = writer.sheets['Sessions']
            summary_sheet = writer.sheets['Summary']
            
            # Auto-adjust column widths
            for sheet in [sessions_sheet, summary_sheet]:
                for column in sheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    sheet.column_dimensions[column[0].column_letter].width = adjusted_width
        
        print(f"Data exported to {output_file}")
        print(f"Total sessions: {total_sessions}")
        print(f"Total duration: {total_duration:.1f} minutes ({total_duration/60:.2f} hours)")
        print(f"Average session: {avg_duration:.1f} minutes")
        
    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")
        raise

def main():
    """Main entry point for the application."""
    try:
        init_log()  # Always initialize log first
        args = parse_args()
        
        if args.command == 'start':
            start_session()
        elif args.command == 'stop':
            end_session()
        elif args.command == 'status':
            show_status()
        elif args.command == 'report':
            generate_report()
        elif args.command == 'export':
            export_to_excel(args.output)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 