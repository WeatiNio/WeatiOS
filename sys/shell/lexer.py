from shell.parse import Parser

class Lexer():
    def __init__(self, kernel):
        self.kernel = kernel

    def tokenise(self, command):
        operation = ""
        args = []
        flags = []
        command_pos = 0

        temp_string = ""

        # print(f"Tokenising '{command}'...")

        for index in range(len(command)):
            char = command[index]
            if char == " " or index == len(command):
                if command_pos == 0:
                    operation = temp_string
                elif temp_string[0] != "-":
                    args.append(temp_string)
                else:
                    flags.append(temp_string)
                
                command_pos += 1
                temp_string = ""
            else:
                temp_string += char        

        if temp_string:
            if command_pos == 0:
                operation = temp_string
            elif temp_string[0] != "-":
                args.append(temp_string)
            else:
                flags.append(temp_string)

        parser = Parser(kernel=self.kernel)
        parser.parse({"operation": operation, "args": args, "flags": flags})