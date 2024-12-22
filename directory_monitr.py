import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DirectoryMonitorHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file

    def on_modified(self, event):
        self.log_event("modified", event)

    def on_created(self, event):
        self.log_event("created", event)

    def on_deleted(self, event):
        self.log_event("deleted", event)

    def log_event(self, event_type, event):
        event_data = {
            "event_type": event_type,
            "file_path": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"Detected {event_type} on {event.src_path}")
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event_data) + "\n")

def main():
    directory_to_watch = "/home/osamah/ubuntu/bsm/test/python"
    log_file = "/home/osamah/ubuntu/bsm/test/logs/changes.json"


    # Ensure log file exists
    open(log_file, 'a').close()

    event_handler = DirectoryMonitorHandler(log_file)
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=True)

    print(f"Monitoring directory: {directory_to_watch}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
