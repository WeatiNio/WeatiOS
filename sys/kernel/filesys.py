import os
import pathlib
import shutil

DISK_PATH = pathlib.Path(__file__).parent.resolve() / "disk"

def real_path(path):
    return rf"{DISK_PATH / path}"

def list_dir(path):
    dirs = []

    for item in os.listdir(real_path(path)):
        full_path = os.path.join(real_path(path), item)
        if os.path.isdir(full_path): dirs.append(item + "\\")
        else: dirs.append(item)    

    return dirs

class LERDCRC:
    def __init__(self):
        if not os.path.exists(DISK_PATH): os.mkdir(DISK_PATH); print(f"{"\033[1m"}[INFO] No disk found, creating new one...")

    def mkfile(self, location, content):
        target = real_path(location)

        with open(target, "w+") as f:
            f.write(content)

    def mkdir(self, location):
        target = real_path(location)

        os.mkdir(target)

    def delete(self, path):
        target = real_path(path)
        print(type(target))
        
        print(os.path.isdir(target))
        
        if os.path.isdir(target): shutil.rmtree(target)
        else: os.remove(target)
        

    def list(self, path):
        target = list_dir(path)
        if target:
            print(f"{"\033[1m"}Listing files...\n")
            for item in target:
                print(item)
        else: print(f"{"\033[1m"}[INFO] No files or directories in 'disk\\{path}'")
            
    def read(self, location):
        target = real_path(location)

        with open(target, "r") as f:
            return f.read()
    
    def edit(self, location, content):
        target = real_path(location)

        if not os.path.exists(target): raise FileNotFoundError()

        with open(target, "w+") as f:
            f.write(content)

    def rename(self, location, name):
        target = real_path(location)
        
        os.rename(target, pathlib.Path(target).parent.absolute() / name)

    def clear(self):
        shutil.rmtree(DISK_PATH)
        os.mkdir(DISK_PATH)