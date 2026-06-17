import time
import requests

def confirm():
    if input(f"{"\033[95m"}[CONFIRM] You are running a risky command. Type 'confirm' to continue: {'\033[0m'}").lower() == "confirm":
        return True
    else:
        print("[INFO] Operation cancelled")
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
    print(ctx["kernel"].filesystem.read(name))

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

            print(f"Shutting down in {timer}s...")
            time.sleep(timer)

        ctx["kernel"].shutdown()

def ping(ctx):
    url = ctx["args"][0]
    response = None

    try:
        response = requests.get(url)
    except Exception:
        print(f"{"\033[93m"}[ERROR] Invalid URL{"\033[0m"}")
        return
    
    elapsed = response.elapsed
    print(f"Response took {int(elapsed.microseconds / 1000)}ms ({elapsed.total_seconds():0.3f}s)")
    if "-headers" in ctx["flags"]:
        print(f"{"\033[95m"}[HEADERS] {response.headers}{"\033[0m"}")
    

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
                print(f"{"\033[93m"}[ERROR] Input file not found{"\033[0m"}")
            except ValueError:
                print(f"{"\033[93m"}[ERROR] Argument contains wrong value type{"\033[0m"}")
            except IndexError:
                print(f"{"\033[93m"}[ERROR] Missing argument{"\033[0m"}")
            except FileExistsError:
                print(f"{"\033[93m"}[ERROR] File already exists{"\033[0m"}")
            except Exception as e:
                print(f"{"\033[93m"}[ERROR] Unknown error: {e}{"\033[0m"}")

        else:
            print(f"{"\033[93m"}[ERROR] Invalid command{"\033[0m"}")