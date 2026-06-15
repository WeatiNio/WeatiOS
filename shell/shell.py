from shell.lexer import Lexer

class Shell:
    def __init__(self, kernel):
        self.running = False
        self.kernel = kernel

    def start(self):
        self.running = True
        while self.running:
            command = input("_>")

            lexer = Lexer(kernel=self.kernel)
            lexer.tokenise(command)