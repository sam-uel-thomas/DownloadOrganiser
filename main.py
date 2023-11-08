import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

downloads_folder = os.path.expanduser('~') + '/Downloads'
destination_folders = {
    ".pdf": os.path.expanduser("~") + "/Downloads/PDF",
    ".docx": os.path.expanduser("~") + "/Downloads/Documents",
    ".png": os.path.expanduser("~") + "/Downloads/Images",
    ".jpg": os.path.expanduser("~") + "/Downloads/Images",
    ".jpeg": os.path.expanduser("~") + "/Downloads/Images",
    ".gif": os.path.expanduser("~") + "/Downloads/Images",
    ".mp4": os.path.expanduser("~") + "/Downloads/Videos",
    ".mp3": os.path.expanduser("~") + "/Downloads/Music",
}
misc_folder = os.path.expanduser("~") + "/Downloads/Misc"

class DownloadSorter(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_extension = os.path.splitext(event.src_path)[-1].lower()
            if file_extension in destination_folders:
                destination_folder = destination_folders[file_extension]
                shutil.move(event.src_path, destination_folder)
            else:
                shutil.move(event.src_path, misc_folder)

if __name__ == "__main__":
    event_handler = DownloadSorter()
    observer = Observer()
    observer.schedule(event_handler, downloads_folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()