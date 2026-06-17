import time
import requests

def confirm():
    if input(f"{"\033[95m"}{"\033[1m"}[WARN] You are running a risky command. Type 'confirm' to continue: {'\033[0m'}").lower() == "confirm":
        return True
    else:
        print(f"{"\033[1m"}[INFO] Operation cancelled")
        return False

def create(ctx):
    name = ctx["args"][0]
    content = " ".join(ctx["args"][1:])
    ctx["kernel"].filesystem.create(name, content)

def delete(ctx):
    name = ctx["args"][0]
    ctx["kernel"].filesystem.delete(name)

def list(ctx):
    ctx["kernel"].filesystem.list()

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

def cleardisk(ctx):
    if "-f" in ctx["flags"] or confirm():
        ctx["kernel"].filesystem.clear()

def shutdown(ctx):
    if "-f" in ctx["flags"] or confirm():
        if ctx["args"]:
            timer = int(ctx["args"][0])

            print(f"{"\033[1m"}Shutting down in {timer}s...")
            time.sleep(timer)

        ctx["kernel"].shutdown()

def ping(ctx):
    url = ctx["args"][0]
    response = None

    try:
        response = requests.get(url)
    except Exception:
        print(f"{"\033[93m"}{"\033[1m"}[ERROR] Invalid URL")
        return
    
    elapsed = response.elapsed
    print(f"{"\033[1m"}{url} responded in {int(elapsed.total_seconds() * 1000)}ms")
    if "-headers" in ctx["flags"] or "-a" in ctx["flags"]:
        print(f"{"\033[94m"}[HEADERS] {response.headers}")
    if "-content" in ctx["flags"] or "-a" in ctx["flags"]:
        print(f"{"\033[92m"}[CONTENT] {response.content.decode()}")

        print(f"{"\033[0m"}{"\033[1m"}[INFO] The '-content' & '-a' flags may take up {"\033[4m"}LOTS{"\033[0m"}{"\033[1m"} of space in your terminal")

    

class Parser:
    def __init__(self, kernel):
         self.kernel = kernel
         self.commands = {
             "create": create,
             "delete": delete,
             "list": list,
             "read": read,
             "cleardisk": cleardisk,
             "shutdown": shutdown,
             "edit": edit,
             "rename": rename,
             "copy": copy,
             "ping": ping
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
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Input file not found")
            except ValueError:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Argument contains wrong value type")
            except IndexError:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Missing argument")
            except FileExistsError:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] File already exists")
            except Exception as e:
                print(f"{"\033[93m"}{"\033[1m"}[ERROR] Unknown error: {e}")

        else:
            print(f"{"\033[93m"}{"\033[1m"}[ERROR] Invalid command")