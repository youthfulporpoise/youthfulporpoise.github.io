from sshkeyboard import listen_keyboard, stop_listening
from colorama import *
from time import time

class Checker:
    '''This class loads the content to be transcribed and checks the inputs of
    the user.'''

    content_file = ""
    content = ""
    content_length = 0
    index = 0
    key_repr = {
        "space": " ",
        "backspace": "\b",
        "tab": "\t",
        "enter": "\n"
    }

    intervals = []  # stores time intervals between key presses
    wpm = 0  # stores WPM

    incorrect_entries = 0
    correct_entries = 0
    accuracy = 0  # stores typing accuracy in percentage

    def __init__(self, content_file="content.txt"):
        self.content_file = content_file
        with open(content_file, 'r') as f:
            self.content = f.read()
            self.content_length = len(self.content)

    def __next__(self) -> str:
        s = self.content[self.index]
        self.index += 1
        return s

    def __prev__(self) -> None:
        self.index -= 1 if self.index > 0 else 0

    def __update__(self) -> None:
        total_entries = self.correct_entries + self.incorrect_entries
        if len(self.intervals) > 10:
            minutes = (self.intervals[-1] - self.intervals[0]) / 60
            self.wpm = (total_entries / 5) / minutes
            self.accuracy = self.correct_entries / total_entries

    def check(self, c: str) -> (bool, str):
        '''Check the if input character is correct, else rubricate and mock.'''

        c = self.key_repr.get(c, c)
        if c == '\b':
            self.__prev__()
            return (self.index == self.content_length, "\b \b")
        else:
            self.__update__()
            self.intervals.append(round(time()))
            if c == self.__next__():
                self.correct_entries += 1
                return (self.index == self.content_length, c)
            else:
                self.incorrect_entries += 1
                return (self.index == self.content_length, Fore.RED + c + Fore.RESET)

    def stats(self) -> (int, int):
        self.__update__()
        return (round(self.wpm), round(self.accuracy * 100))


# Press and release event actions.
content_file = "content.txt"
checker = Checker(content_file)
def on_press(key):
    is_finished, key = checker.check(key)
    print(key, end='', flush=True)

    if is_finished:
        print(Fore.BLUE + "\nTest Complete" + Fore.RESET)
        wpm, accuracy = checker.stats()
        print(f"WPM: {wpm}\nAccuracy: {accuracy}%")
        stop_listening()

def on_release(key):
    pass

# Here follows the start of execution.
def main():
    try:
        with open(content_file) as f:
            txt = f.read()
            txt = "\n\t" + txt.replace("\n", "\n\t")
            print(txt, flush=True)

        listen_keyboard(
                on_press=on_press,
                on_release=on_release,
                delay_second_char=0.1)

    except KeyboardInterrupt:
        print("Quitting ...")
        exit(0);

    except ValueError:
        print("Quitting ...")
        exit(0)


if __name__ == "__main__":
    main()
