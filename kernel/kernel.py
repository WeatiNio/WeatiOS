import sys

from shell.shell import Shell
from kernel.filesys import FileSystem

class Kernel:
    def __init__(self):
        print("Kernel created!")

        self.filesystem = FileSystem()

    def boot(self):
        py_version = sys.version_info
        print(f"Booting WeatiOS with Python version '{py_version.major}.{py_version.minor}.{py_version.micro}'...\n")

        shell = Shell(kernel=self)
        shell.start()

    def shutdown(self):
        exit()