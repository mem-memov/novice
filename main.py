import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ExampleDirectoryHandler(FileSystemEventHandler):
    """Handles file system events in the example directory."""

    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"File created: {event.src_path}")
        else:
            logger.info(f"Directory created: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            logger.info(f"File deleted: {event.src_path}")
        else:
            logger.info(f"Directory deleted: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            logger.info(f"File modified: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            logger.info(f"File moved: {event.src_path} -> {event.dest_path}")
        else:
            logger.info(f"Directory moved: {event.src_path} -> {event.dest_path}")


def main():
    # Define the directory to watch
    watch_directory = Path(__file__).parent / "example"
    
    # Ensure the directory exists
    watch_directory.mkdir(exist_ok=True)
    
    logger.info(f"Starting watcher for directory: {watch_directory.resolve()}")

    # Set up the observer
    event_handler = ExampleDirectoryHandler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_directory), recursive=True)

    # Start the observer
    observer.start()
    logger.info("Watcher started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Watcher stopped.")
    
    observer.join()


if __name__ == "__main__":
    main()
