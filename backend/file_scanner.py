import os
from pathlib import Path
from utils import get_file_extension, get_category

def scan_folder(folder_path: str):
    """Scan folder and return counts per category."""
    counts = {
        "Images": 0,
        "Documents": 0,
        "Videos": 0,
        "Code": 0,
        "Others": 0
    }
    total = 0
    root = Path(folder_path)
    if not root.exists() or not root.is_dir():
        raise ValueError("Invalid folder path")

    for item in root.iterdir():
        if item.is_file():
            ext = get_file_extension(item.name)
            category = get_category(ext)
            counts[category] = counts.get(category, 0) + 1
            total += 1

    return counts, total