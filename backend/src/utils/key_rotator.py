import threading
from typing import List

class ApiKeyRotator:
    def __init__(self, keys: List[str]):
        self.keys = keys
        self.current_index = 0
        self.lock = threading.Lock()

    def get_next_key(self):
        with self.lock:
            if not self.keys:
                return None
            key = self.keys[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.keys)
            return key 