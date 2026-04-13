import logging
from watchdog.events import FileSystemEventHandler

class ExampleDirectoryHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
    
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
        else:
            logging.info(f"Directory created: {event.src_path}")
    
    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")
        else:
            logging.info(f"Directory deleted: {event.src_path}")
    
    def on_moved(self, event):
        src_path = event.src_path
        dest_path = event.dest_path
        
        # Check if it's a rename (same parent directory) or a move (different parent)
        import os
        src_dir = os.path.dirname(src_path)
        dest_dir = os.path.dirname(dest_path)
        
        if src_dir == dest_dir:
            if event.is_directory:
                logging.info(f"Directory renamed: {src_path} -> {dest_path}")
            else:
                logging.info(f"File renamed: {src_path} -> {dest_path}")
        else:
            if event.is_directory:
                logging.info(f"Directory moved: {src_path} -> {dest_path}")
            else:
                logging.info(f"File moved: {src_path} -> {dest_path}")
