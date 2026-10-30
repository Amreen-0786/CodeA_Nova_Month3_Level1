# Log Analyzer Tool

## Objective
Read application/server logs, parse timestamp and severity, count log levels, list errors and warnings, and create summary reports.

## Supported line format
`YYYY-MM-DD HH:MM:SS LEVEL message`

Example:
`2026-10-30 09:10:00 ERROR Database connection failed`

Supported levels: DEBUG, INFO, WARNING, ERROR and CRITICAL.

## Run
From this folder:
```powershell
python log_analyzer.py --input sample_logs\server.log
```
Choose another output directory:
```powershell
python log_analyzer.py --input sample_logs\server.log --output reports
```

The program creates:
- `reports/log_summary.txt` — readable summary.
- `reports/log_summary.json` — structured results for other tools.

Unrecognized non-empty lines are counted as malformed instead of crashing the program.
