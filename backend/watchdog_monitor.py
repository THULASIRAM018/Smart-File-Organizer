import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file_organizer import organize_folder

class OrganizeHandler(FileSystemEventHandler):
    """Event handler that organizes new files."""
    def __init__(self, folder_to_watch):
        self.folder_to_watch = folder_to_watch

    def on_created(self, event):
        # Avoid organizing directories or temporary files
        if not event.is_directory and not event.src_path.endswith('.tmp'):
            # Give a small delay to ensure file is fully written
            time.sleep(1)
            try:
                organize_folder(self.folder_to_watch)
                print(f"Organized new file in {self.folder_to_watch}")
            except Exception as e:
                print(f"Error organizing after file creation: {e}")

# Global dictionary to keep track of observers
_observers = {}

def start_monitoring(folder_path: str):
    """Start a watchdog observer for the given folder."""
    if folder_path in _observers:
        return  # already watching

    event_handler = OrganizeHandler(folder_path)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)  # only top-level
    observer.start()
    _observers[folder_path] = observer
    print(f"Started monitoring {folder_path}")

def stop_monitoring(folder_path: str = None):
    """Stop a specific observer or all if folder_path is None."""
    if folder_path is None:
        for path, obs in list(_observers.items()):
            obs.stop()
            obs.join()
            del _observers[path]
    else:
        obs = _observers.get(folder_path)
        if obs:
            obs.stop()
            obs.join()
            del _observers[folder_path]