import time
from pathlib import Path


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class SoftwareSingleton:
    def __init__(self, lock_file: Path):
        self.lock_file = lock_file
        self._create_lock_file()

    def _create_lock_file(self):
        if self.lock_file.exists():
            print("Another instance is already running. Exiting.")
            while self.lock_file.exists():
                time.sleep(0.2)
        else:
            self.lock_file.touch()

    def __del__(self):
        if self.lock_file.exists():
            self.lock_file.unlink()
