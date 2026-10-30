# Code-A-Nova Month 3 — Level 1 Python Projects

This bundle contains two standalone command-line projects:

1. **File Organizer** — sorts files into folders by extension.
2. **Log Analyzer** — parses log entries, counts INFO/WARNING/ERROR levels, and writes summary reports.

## Requirements
- Python 3.10 or newer
- No third-party packages required

## Run in VS Code (Windows PowerShell)
Open this extracted folder in VS Code, then open Terminal → New Terminal.

### Project 1: File Organizer
```powershell
cd File-Organizer
python file_organizer.py --source sample_files --dry-run
```
If the preview looks right, actually move the files:
```powershell
python file_organizer.py --source sample_files
```
To organize a different folder:
```powershell
python file_organizer.py --source "C:\Users\YourName\Downloads" --dry-run
```
Remove `--dry-run` only after checking the preview. Files with unknown extensions go to `Others`. Existing filenames are never overwritten; a numbered name is chosen instead.

### Project 2: Log Analyzer
Open a new terminal (or return to the root folder):
```powershell
cd ..\Log-Analyzer
python log_analyzer.py --input sample_logs\server.log
```
Create text and JSON reports:
```powershell
python log_analyzer.py --input sample_logs\server.log --output reports
```

## Project contents
- Each project has its own README with features and usage.
- Sample input files are included.
- `tests` contains standard-library unit tests.
- The projects do not need `pip install`.

## Safety
Always preview file movements with `--dry-run` before organizing a real folder. The organizer does not delete files.
