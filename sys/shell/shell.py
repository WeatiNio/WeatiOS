from shell.lexer import Lexer

class Shell:
    def __init__(self, kernel):
        self.running = False
        self.kernel = kernel

    def start(self):
        self.running = True
        while self.running:
            cd = str(self.kernel.filesystem.get_cd())
            display = cd
            if cd == ".": display = "\\"
            else: display = cd + "\\"

            command = input(f"{"\033[0m"}{display}> ")

            lexer = Lexer(kernel=self.kernel)
            lexer.tokenise(command)