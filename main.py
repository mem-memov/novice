import logging
from pathlib import Path
from threading import Event
from watchdog.observers import Observer

from src.handler import ExampleDirectoryHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


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

    stop_event = Event()
    try:
        stop_event.wait()  # Block efficiently until interrupted
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        logger.info("Watcher stopped.")
    
    observer.join()


if __name__ == "__main__":
    main()
