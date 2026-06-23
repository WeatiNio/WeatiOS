import os
import pathlib
import shutil

DISK_PATH = pathlib.Path(__file__).parent.resolve() / "disk"
CD = DISK_PATH

def update_cd(path):
    global CD

    if path: new = DISK_PATH / path
    else: new = DISK_PATH

    if not os.path.isdir(new): 
        print(f"{"\033[93m"}{"\033[1m"}[ERROR] Directory doesn't exist") 
        return

    CD = new

def real_path(path):
    return rf"{CD / path}"

def virtual_path(path):
    v_path = pathlib.Path(path).relative_to(DISK_PATH)
    
    if v_path == ".": print("root disk")
    return v_path

def list_dir(path):
    dirs = []

    for item in os.listdir(real_path(path)):
        full_path = os.path.join(real_path(path), item)
        if os.path.isdir(full_path): dirs.append(item + "\\")
        else: dirs.append(item)    

    return dirs

class LERDCRMC:
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
        
        if os.path.isdir(target): shutil.rmtree(target)
        else: os.remove(target)
        

    def list(self, path):
        target = list_dir(path)
        if target:
            print(f"{"\033[1m"}Listing items...\n")
            for item in target:
                print(item)
        else: print(f"{"\033[1m"}[INFO] No items found")
            
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
        global CD

        shutil.rmtree(DISK_PATH)
        os.mkdir(DISK_PATH)

        CD = DISK_PATH

    def move(self, file, destination):
        target_file = real_path(file)
        target = real_path(destination)

        if os.path.isdir(target_file):
            print(f"{"\033[93m"}{"\033[1m"}[ERROR] This is a directory!")
            return
        
        with open(pathlib.Path(target) / pathlib.Path(target_file).name, "w") as f:
            f.write(self.read(file))
        os.remove(target_file)

    def cd(self, location):
        update_cd(location)

    def get_cd(self):
        return virtual_path(CD)