class FileSystem:
    def __init__(self):
        print("Filesystem created!")

        self.files = {}

    def create(self, name, content):
        self.files[name] = content

    def list(self):
        print("Listing files...\n")
        for name, content in self.files.items():
            print(f"'{name}': {content}")
            

    def read(self, name):
        if name not in self.files:
            raise FileNotFoundError(f"{name} does not exist")
        
        return self.files[name]