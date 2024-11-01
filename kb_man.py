from sshkeyboard import listen_keyboard
from queue import SimpleQueue
from colorama import *

class Checker:
    '''This class loads the content to be transcribed and checks the inputs of
    the user.'''

    content_file = ""
    content = ""
    index = 0

    def __init__(self, content_file="content.txt"):
        self.content_file = content_file
        with open(content_file, 'r') as f:
            self.content = f.read()

    def __next__(self) -> str:
        s = self.content[self.index]
        self.index += 1
        return s

    def __prev__(self) -> None:
        self.index -= 1 if self.index > 0 else 0

    def check(self, c: str) -> str:
        '''Check the if input character is correct, else rubricate and mock.'''
        if c == '\b':
            self.__prev__()
            return "\b \b"
        elif c == self.__next__():
            return c
        else:
            return Fore.RED + c + Fore.RESET


key_repr = {
    "space": " ",
    "backspace": "\b",
    "tab": "\t",
    "enter": "\n"
}

# Press and release event actions.
content_file = "content.txt"
checker = Checker(content_file)
def on_press(key):
    k = key_repr.get(key, key)
    k = checker.check(k)
    print(k, end='', flush=True)

def on_release(key):
    pass

# Here follows the start of execution.
def main():
    try:
        with open(content_file) as f:
            print(f.read() + "\n", flush=True)
        listen_keyboard(
                on_press=on_press,
                on_release=on_release,
                delay_second_char=0.1)
    except KeyboardInterrupt:
        print("Quitting ...")
        exit(0);

if __name__ == "__main__":
    main()
