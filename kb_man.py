from sshkeyboard import listen_keyboard
from queue import SimpleQueue
from colorama import *

class Checker:
    '''This class loads the content to be transcribed and checks the inputs of
    the user.'''

    content_file = ""
    queue = Queue()

    def __init__(content_file="content.txt"):
        self.content_file = content_file
        with open(content_file, 'r') as f:
            txt = f.read()
            for s in txt:
                queue.put(s, False)

    def check(c: str):
        '''Check the if input character is correct, else rubricate and mock.'''
        if c == queue.get(False):
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
def on_press(key):
    k = key_repr.get(key, key)
    if k == "\b":
        print(f"\b \b", end='', flush=True)
    else:
        print(k, end='', flush=True)

def on_release(key):
    pass

# Here follows the start of execution.
def main():
    try:
        listen_keyboard(
                on_press=on_press,
                on_release=on_release,
                delay_second_char=0.1)
    except KeyboardInterrupt:
        print("\nQuitting ...")
        exit(0);

if __name__ == "__main__":
    main()
