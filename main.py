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


    def finished_download(self, file_path):
        while True:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                time.sleep(5)
                if file_size == os.path.getsize(file_path):
                    return True
            else:
                return False

    def on_modified(self, event):
        if os.path.basename(event.src_path).startswith(".company") or os.path.basename(event.src_path).endswith(".crdownload") or os.path.basename(event.src_path) == ".DS_STORE":
            return
        
        if not event.is_directory:
            file_extension = os.path.splitext(event.src_path)[-1].lower()
            if file_extension in destination_folders:
                destination_folder = destination_folders[file_extension]
                destination_path = os.path.join(destination_folder, os.path.basename(event.src_path))
                if self.finished_download(event.src_path):
                    if not os.path.exists(destination_path):
                        shutil.move(event.src_path, destination_path)
                    else:
                        base_name, ext = os.path.splitext(os.path.basename(event.src_path))
                        count = 1
                        while os.path.exists(destination_path):
                            new_base_name = f"{base_name} ({count})"
                            destination_path = os.path.join(destination_folder, f"{new_base_name}{ext}")
                            count += 1
                        shutil.move(event.src_path, destination_path)
            else:
                if not os.path.exists(misc_folder):
                    shutil.move(event.src_path, misc_folder)
                else:
                    base_name, ext = os.path.splitext(os.path.basename(event.src_path))
                    count = 1
                    while os.path.exists(misc_folder):
                        new_base_name = f"{base_name} ({count})"
                        destination_path = os.path.join(misc_folder, f"{new_base_name}{ext}")
                        count += 1
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