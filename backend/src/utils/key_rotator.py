import threading
from typing import List
import logging

class ApiKeyRotator:
    def __init__(self, keys: List[str]):
        self.keys = keys
        self.current_index = 0
        self.lock = threading.Lock()
        logging.info(f"Initialized ApiKeyRotator with {len(keys)} keys")
        
    def get_next_key(self):
        with self.lock:
            if not self.keys:
                logging.warning("No API keys available in the rotator")
                return None
                
            key = self.keys[self.current_index]
            # Mask most of the key for security in logs
            masked_key = f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "***"
            
            logging.info(f"Using key {self.current_index + 1} of {len(self.keys)}: {masked_key}")
            print(f"Rotating to key {self.current_index + 1} of {len(self.keys)}: {masked_key}")
            
            # Rotate to next key
            self.current_index = (self.current_index + 1) % len(self.keys)
            return key 