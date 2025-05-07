# Focus Tracker

A simple command-line tool for tracking focused work time. This tool helps you log your focused work sessions and generate reports of your total focused time.

## Installation

### From GitHub (Recommended)

1. Install uv if you haven't already:
```powershell
pip install uv
```

2. Create a virtual environment and install the package:
```powershell
uv venv
.venv\Scripts\activate
uv pip install git+https://github.com/serband/focus-tracker.git
```

Or using pip:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install git+https://github.com/serband/focus-tracker.git
```

## Usage

After installation, activate your virtual environment and use these commands:

```powershell
# Start a new session
focus-tracker start

# Check current status
focus-tracker status

# End current session
focus-tracker stop

# View total focused time
focus-tracker report
```

## Data Storage

The tool stores your focus session data in a CSV file located at `~/.focus_log.csv`. The file contains the following columns:
- Start Time
- End Time
- Duration (minutes)

## Requirements

- Python 3.8 or higher
- uv (optional, but recommended for faster installation)

## Development

If you're developing the package:

1. Clone the repository:
```powershell
git clone https://github.com/serband/focus-tracker.git
cd focus-tracker
```

2. Create a virtual environment:
```powershell
uv venv
```

3. Activate it:
```powershell
.venv\Scripts\activate
```

4. Install in development mode:
```powershell
uv pip install -e .
```
