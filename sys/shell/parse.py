import os
import time
import requests

def confirm():
    if input(f"{"\033[95m"}{"\033[1m"}[WARN] You are running a risky command. Type 'confirm' to continue: {'\033[0m'}").lower() == "confirm":
        return True
    else:
        print(f"{"\033[1m"}[INFO] Operation cancelled")
        return False

def mkfile(ctx):
    location = ctx["args"][0]
    content = " ".join(ctx["args"][1:])
    try:
        ctx["kernel"].filesystem.mkfile(location, content)
    except Exception:
        print(f"{"\033[93m"}{"\033[1m"}[ERROR] A file/directory exists with the same name")

def mkdir(ctx):
    location = ctx["args"][0]
    try:
        ctx["kernel"].filesystem.mkdir(location)
    except:
        print(f"{"\033[93m"}{"\033[1m"}[ERROR] A file/directory exists with the same name")

def delete(ctx):
    location = ctx["args"][0]
    ctx["kernel"].filesystem.delete(location)

def list(ctx):
    dir = ""
    try:
        dir = ctx["args"][0]
    except:
        dir = ""

    ctx["kernel"].filesystem.list(dir)

def read(ctx):
    name = ctx["args"][0]
    print(f"{"\033[1m"}{ctx["kernel"].filesystem.read(name)}")

def edit(ctx):
    name = ctx["args"][0]
    new = " ".join(ctx["args"][1:])
    ctx["kernel"].filesystem.edit(name, new)

def rename(ctx):
    old = ctx["args"][0]
    new = ctx["args"][1]
    ctx["kernel"].filesystem.rename(old, new)

def copy(ctx):
    original = ctx["args"][0]
    new = ctx["args"][1]
    ctx["kernel"].filesystem.create(new, ctx["kernel"].filesystem.read(original))

def clrdisk(ctx):
    if "-f" in ctx["flags"] or confirm():
        ctx["kernel"].filesystem.clear()

def shutdown(ctx):
    if "-f" in ctx["flags"] or confirm():
        if ctx["args"]:
            timer = int(ctx["args"][0])

            print(f"{"\033[1m"}Shutting down in {timer}s...{'\033[0m'} ")
            time.sleep(timer)

        ctx["kernel"].shutdown()

def cmds(ctx):
    commands = Parser(ctx["kernel"]).commands
    print(f"{"\033[1m"}Listing commands...\n")
    for cmd in commands:
        print(cmd)

def echo(ctx):
    string = ""
    for word in ctx["args"]:
        for char in word:
            string += char
        
        string += " "

    print(string)

def clear(ctx):
    os.system("cls" if os.name == "nt" else "clear")

def ping(ctx):
    url = ctx["args"][0]
    response = None

    try:
        response = requests.get(url)
    except Exception:
        print(f"{"\033[93m"}{"\033[1m"}[ERROR] Invalid URL")
        return
    
    elapsed = response.elapsed
    print(f"'{"\033[1m"}{url}' responded in {int(elapsed.total_seconds() * 1000)}ms")
    if "-headers" in ctx["flags"] or "-a" in ctx["flags"]:
        print(f"{"\033[94m"}[HEADERS] {response.headers}")
    if "-content" in ctx["flags"] or "-a" in ctx["flags"]:
        print(f"{"\033[92m"}[CONTENT] {response.content.decode()}")

        print(f"{"\033[0m"}{"\033[1m"}[INFO] The '-content' & '-a' flags may take up {"\033[4m"}LOTS{"\033[0m"}{"\033[1m"} of space in your terminal")

class Parser:
    def __init__(self, kernel):
         self.kernel = kernel
         self.commands = {
             "mkfile": mkfile,
             "mkdir": mkdir,
             "delete": delete,
             "list": list,
             "read": read,
             "clrdisk": clrdisk,
             "shutdown": shutdown,
             "edit": edit,
             "rename": rename,
             "copy": copy,
             "ping": ping,
             "echo": echo,
             "clear": clear,
             "cmds": cmds
         }

    def parse(self, tokens):
        # print(f"Parsing '{tokens}'...")

        operation = tokens["operation"]
        args = tokens["args"]
        flags = tokens["flags"]

        if operation in self.commands:
            try:
                self.commands[operation]({"args": args, "flags": flags, "kernel": self.kernel})
            except FileNotFoundError:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Input file/directory not found")
            except ValueError:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Argument contains wrong value type")
            except IndexError:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Missing argument")
            except FileExistsError:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] File already exists")
            except PermissionError:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Permission denied")
            except Exception as e:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Unknown error: {e}")

        else:
            print(f"{"\033[93m"}{"\033[1m"}[ERROR] Invalid command")