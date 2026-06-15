def create(args, kernel):
    name = args[0]
    content = " ".join(args[1:])
    kernel.filesystem.create(name, content)

def list(args, kernel):
    kernel.filesystem.list()

def read(args, kernel):
    name = args[0]
    print(kernel.filesystem.read(name))

def shutdown(args, kernel):
    kernel.shutdown()

class Parser:
    def __init__(self, kernel):
         self.kernel = kernel
         self.commands = {
             "create": create,
             "list": list,
             "read": read,
             "shutdown": shutdown
         }

    def parse(self, tokens):
        # print(f"Parsing '{tokens}'...")

        operation = tokens["operation"]
        args = tokens["args"]

        if operation in self.commands:
            try:
                self.commands[operation](args, self.kernel)
            except Exception as e:
                print(f"Unable to run command: {e}")
        else:
            print("Unknown command")