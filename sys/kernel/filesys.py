import os
import json
import pathlib

DISK_PATH = pathlib.Path(__file__).parent.resolve() / "disk.json"

def read_disk():
    if not os.path.exists(DISK_PATH):
        with open(DISK_PATH, "w+") as f:
            json.dump({}, f, indent=4)

    with open(DISK_PATH, "r") as f:
        data = json.load(f)

    return data

def save_disk(data):
    with open(DISK_PATH, "w") as f:
        json.dump(data, f, indent=4)

class LERDCRC:
    def __init__(self):
        self.temp_disk = read_disk()

    def create(self, name, content):
        if not name in self.temp_disk:
            self.temp_disk[name] = content
            self.save()
        else:
            raise FileExistsError()

    def delete(self, name):
        if name not in self.temp_disk:
            raise FileNotFoundError()
        
        del self.temp_disk[name]
        self.save()

    def list(self):
        print("Listing files...\n")
        for name, content in read_disk().items():
            print(f"'{name}': {content}")
            
    def read(self, name):
        if name not in self.temp_disk:
            raise FileNotFoundError()
        
        return self.temp_disk[name]
    
    def edit(self, name, new):
        if name not in self.temp_disk:
            raise FileNotFoundError()
        
        self.temp_disk[name] = new
        self.save()

    def rename(self, old, new):
        if old not in self.temp_disk:
            raise FileNotFoundError()
        
        self.temp_disk[new] = self.temp_disk.pop(old)
        self.save()
    
    def save(self):
        save_disk(self.temp_disk)

    def clear(self):
        save_disk({})
        self.temp_disk = {}