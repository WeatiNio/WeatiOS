def split_path(path):
    split = []

class FileSystem:
    def __init__(self):
        self.files = {}

    def create(self, name, content):
        if not name in self.files:
            self.files[name] = content
        else:
            raise FileNotFoundError()

    def delete(self, name):
        if name not in self.files:
            raise FileNotFoundError()
        
        del self.files[name]

    def list(self):
        print("Listing files...\n")
        for name, content in self.files.items():
            print(f"'{name}': {content}")
            
    def read(self, name):
        if name not in self.files:
            raise FileNotFoundError()
        
        return self.files[name]