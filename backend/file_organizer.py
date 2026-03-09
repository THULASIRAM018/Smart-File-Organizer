import os
import shutil
from pathlib import Path
from utils import get_file_extension, get_category

def organize_folder(folder_path: str):
    """Move files into subfolders based on category."""
    root = Path(folder_path)
    if not root.exists() or not root.is_dir():
        raise ValueError("Invalid folder path")

    # Create category folders if they don't exist
    categories = ["Images", "Documents", "Videos", "Code", "Others"]
    for cat in categories:
        (root / cat).mkdir(exist_ok=True)

    moved_count = 0
    for item in root.iterdir():
        if item.is_file():
            ext = get_file_extension(item.name)
            category = get_category(ext)
            dest_dir = root / category
            dest_path = dest_dir / item.name

            # Handle name collisions by adding a number
            if dest_path.exists():
                base = item.stem
                suffix = item.suffix
                counter = 1
                while dest_path.exists():
                    new_name = f"{base}_{counter}{suffix}"
                    dest_path = dest_dir / new_name
                    counter += 1

            shutil.move(str(item), str(dest_path))
            moved_count += 1

    return moved_count