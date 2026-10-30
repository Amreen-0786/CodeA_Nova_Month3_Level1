# File Organizer Script

## Objective
Sort files in a chosen directory into folders based on file extensions.

## Features
- Scans files in the selected directory (does not recurse into subfolders).
- Recognizes images, documents, videos, audio, archives and code files.
- Places unrecognized extensions in `Others`.
- Supports a safe preview using `--dry-run`.
- Avoids overwriting files by creating names such as `report_1.pdf`.
- Does not delete files.

## Run
Preview first:
```powershell
python file_organizer.py --source sample_files --dry-run
```
Move files:
```powershell
python file_organizer.py --source sample_files
```
For Downloads:
```powershell
python file_organizer.py --source "$HOME\Downloads" --dry-run
```

## Main concepts
`pathlib` handles paths, `shutil.move()` moves files, dictionaries/sets map extensions to categories, and `argparse` reads command-line options.
