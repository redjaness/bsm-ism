import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        log_path = "/home/kali/bsm/logs/changes.json"
        change = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "is_directory": event.is_directory,
            "time": time.ctime()
        }
        if not os.path.exists(log_path):
            with open(log_path, "w") as f:
                json.dump([], f)

        with open(log_path, "r+") as f:
            logs = json.load(f)
            logs.append(change)
            f.seek(0)
            json.dump(logs, f, indent=4)

def main():
    path = "/home/kali/bsm/test"
    os.makedirs(path, exist_ok=True)
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
