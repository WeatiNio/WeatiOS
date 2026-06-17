import sys
import threading

from shell.shell import Shell
from kernel.filesys import LERDCRC

class Kernel:
    def __init__(self):
        self.filesystem = LERDCRC()

    def boot(self):
        py_version = sys.version_info
        print(f"Booting WeatiOS with Python version '{py_version.major}.{py_version.minor}.{py_version.micro}'...\n")

        shell = Shell(kernel=self)
        
        shell_thread = threading.Thread(target=shell.start)
        shell_thread.start()

    def shutdown(self):
        self.filesystem.save()
        exit()