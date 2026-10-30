"""Analyze plain-text application logs and create summary reports."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+(?P<message>.*)$",
    re.IGNORECASE,
)

def analyze_log(input_path: Path) -> dict:
    """Parse log lines and return counts, messages, and malformed-line details."""
    if not input_path.exists():
        raise FileNotFoundError(f"Log file not found: {input_path}")
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")

    counts = Counter({level: 0 for level in LEVELS})
    entries = []
    malformed = []

    with input_path.open("r", encoding="utf-8", errors="replace") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line:
                continue
            match = LOG_PATTERN.match(line)
            if not match:
                malformed.append({"line_number": line_number, "line": line})
                continue
            entry = match.groupdict()
            entry["level"] = entry["level"].upper()
            entry["line_number"] = line_number
            counts[entry["level"]] += 1
            entries.append(entry)

    total = len(entries)
    return {
        "source_file": str(input_path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_entries": total,
        "counts": dict(counts),
        "error_messages": [e for e in entries if e["level"] in ("ERROR", "CRITICAL")],
        "warning_messages": [e for e in entries if e["level"] == "WARNING"],
        "malformed_lines": malformed,
        "entries": entries,
    }

def write_reports(result: dict, output_dir: Path) -> tuple[Path, Path]:
    """Write human-readable TXT and machine-readable JSON reports."""
    output_dir.mkdir(parents=True, exist_ok=True)
    txt_path = output_dir / "log_summary.txt"
    json_path = output_dir / "log_summary.json"

    lines = [
        "========== LOG ANALYZER ==========",
        f"Source file       : {result['source_file']}",
        f"Generated at      : {result['generated_at']}",
        f"Total log entries : {result['total_entries']}",
        "",
        "Log level counts:",
    ]
    for level in LEVELS:
        lines.append(f"{level:<18}: {result['counts'].get(level, 0)}")
    lines += ["", "Error / Critical details:"]
    if result["error_messages"]:
        for number, entry in enumerate(result["error_messages"], start=1):
            lines.append(f"{number}. [{entry['level']}] {entry['message']}")
    else:
        lines.append("No errors found.")
    lines += ["", "Warning details:"]
    if result["warning_messages"]:
        for number, entry in enumerate(result["warning_messages"], start=1):
            lines.append(f"{number}. {entry['message']}")
    else:
        lines.append("No warnings found.")
    lines += ["", f"Malformed lines: {len(result['malformed_lines'])}",
              "========== ANALYSIS COMPLETE =========="]
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return txt_path, json_path

def main() -> None:
    parser = argparse.ArgumentParser(description="Count and summarize application log messages.")
    parser.add_argument("--input", required=True, help="Path to a .log or text log file.")
    parser.add_argument("--output", default="reports", help="Directory for generated TXT and JSON reports.")
    args = parser.parse_args()
    try:
        result = analyze_log(Path(args.input))
        txt_path, json_path = write_reports(result, Path(args.output))
        print("========== LOG ANALYZER ==========")
        print(f"Total Log Entries : {result['total_entries']}")
        for level in LEVELS:
            print(f"{level:<18}: {result['counts'].get(level, 0)}")
        print(f"Malformed Lines   : {len(result['malformed_lines'])}")
        print(f"\nText report : {txt_path.resolve()}")
        print(f"JSON report : {json_path.resolve()}")
        print("========== ANALYSIS COMPLETE ==========")
    except (OSError, ValueError) as error:
        parser.error(str(error))

if __name__ == "__main__":
    main()
