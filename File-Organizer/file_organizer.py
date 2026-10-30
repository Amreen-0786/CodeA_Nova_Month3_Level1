"""Organize files in a directory into folders based on file extensions."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ipynb", ".sql"},
}

def category_for(file_path: Path) -> str:
    """Return the category folder for a file based on its suffix."""
    suffix = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"

def unique_destination(destination: Path) -> Path:
    """Avoid overwriting an existing file by adding a numeric suffix."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1

def organize_directory(source: Path, dry_run: bool = True) -> list[tuple[Path, Path]]:
    """
    Organize immediate files in source (not subfolders).
    Returns a list of (original_path, destination_path) pairs.
    """
    source = source.expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")
    if not source.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source}")

    moves: list[tuple[Path, Path]] = []
    for item in sorted(source.iterdir()):
        if not item.is_file():
            continue
        category_dir = source / category_for(item)
        destination = unique_destination(category_dir / item.name)
        moves.append((item, destination))
        print(f"{'[DRY RUN] ' if dry_run else ''}{item.name} -> {category_dir.name}/{destination.name}")
        if not dry_run:
            category_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
    return moves

def main() -> None:
    parser = argparse.ArgumentParser(description="Sort files into folders based on their extensions.")
    parser.add_argument("--source", required=True, help="Directory whose immediate files should be organized.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving any files.")
    args = parser.parse_args()
    try:
        moves = organize_directory(Path(args.source), dry_run=args.dry_run)
        action = "would be organized" if args.dry_run else "organized"
        print(f"\nComplete: {len(moves)} file(s) {action}.")
        if args.dry_run:
            print("Review the preview, then run again without --dry-run to move files.")
    except (OSError, ValueError) as error:
        parser.error(str(error))

if __name__ == "__main__":
    main()
