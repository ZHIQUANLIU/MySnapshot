import os
import datetime
import json
from pathlib import Path
from PIL import Image

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.data = {"last_collection": "Default"}
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.data.update(json.load(f))
            except:
                pass

    def save(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f)

    def get_last_collection(self):
        return self.data.get("last_collection", "Default")

    def set_last_collection(self, name):
        self.data["last_collection"] = name
        self.save()

class StorageManager:
    def __init__(self):
        # Default to Pictures/MySnapshot
        self.base_path = Path(os.path.expanduser("~/Pictures/MySnapshot"))
        
        # Load config
        self.config = ConfigManager(self.base_path / "config.json")
        self.current_collection = self.config.get_last_collection()
        
        self._ensure_paths()

    def _ensure_paths(self):
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True)
        
        col_path = self.get_collection_path()
        if not col_path.exists():
            col_path.mkdir(parents=True)

    def set_collection(self, name):
        self.current_collection = name
        self.config.set_last_collection(name)
        self._ensure_paths()

    def get_collection_path(self):
        return self.base_path / self.current_collection

    def get_all_collections(self):
        if not self.base_path.exists():
            return []
        return [d.name for d in self.base_path.iterdir() if d.is_dir() and d.name != "config.json"]

    def generate_filename(self):
        # Using YYYYMMDDHHMMSS as requested
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{timestamp}.png"

    def save_image(self, image, filename=None):
        if filename is None:
            filename = self.generate_filename()
        
        path = self.get_collection_path() / filename
        image.save(path, "PNG")
        return path

    def delete_image(self, filename):
        path = self.get_collection_path() / filename
        if path.exists():
            os.remove(path)
            return True
        return False

    def delete_collection(self, name):
        import shutil
        col_path = self.base_path / name
        if col_path.exists() and col_path.is_dir():
            shutil.rmtree(col_path)
            # If we deleted the current collection, reset to Default
            if self.current_collection == name:
                self.set_collection("Default")
            return True
        return False

# Global singleton
storage = StorageManager()
