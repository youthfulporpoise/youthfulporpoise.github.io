import asyncio
import micropip

def install_nava():
    await micropip.install("nava")
install_nava()

from nava import play, stop
from sshkeyboard import listen_keyboard, stop_listening
from colorama import *
from time import time
from os import listdir
from random import choice
from yaml import safe_load

class Checker:
    '''This class loads the content to be transcribed and checks the inputs of
    the user.'''

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

    incorrect_seq = 0  # counts the number mistakes the user makes sequentially
    incorrect_entries = 0
    correct_entries = 0
    accuracy = 0  # stores typing accuracy in percentage

    flavour = ""
    audios = {}

    def __init__(self, content, flavour="light"):
        self.content = content

        self.flavour = flavour
        self.audios = {
                "bad": listdir(f"res/{self.flavour}/error/s1"),
                "serious": listdir(f"res/{self.flavour}/error/s2"),
                "grave": listdir(f"res/{self.flavour}/error/s3"),
                "appreciate": listdir(f"res/{self.flavour}/appreciation")
                # "insult": listdir(f"res/{self.flavour}/insult")
        }

    def __next__(self) -> str:
        s = self.content[self.index]
        self.index += 1
        return s

    def __prev__(self) -> None:
        self.index -= 1 if self.index > 0 else 0

    def __update__(self) -> None:
        '''Updates WPM and accuracy.'''

        total_entries = self.correct_entries + self.incorrect_entries
        if len(self.intervals) > 10:
            minutes = (self.intervals[-1] - self.intervals[0]) / 60
            self.wpm = (total_entries / 5) / minutes
            self.accuracy = self.correct_entries / total_entries

    def __comment_on_error__(self):
        if self.incorrect_seq == 1:
            # print(f"res/{self.flavour}/error/s1/{choice(self.audios['bad'])}")
            self.sound_id = play(f"res/{self.flavour}/error/s1/{choice(self.audios['bad'])}",
                 async_mode=True)
        elif 1 < self.incorrect_seq < 3: 
            # stop(self.sound_id)
            self.sound_id = play(f"res/{self.flavour}/error/s2/{choice(self.audios['serious'])}",
                 async_mode=True)
        elif 3 < self.incorrect_seq < 5:
            # stop(self.sound_id)
            self.sound_id = play(f"res/{self.flavour}/error/s3/{choice(self.audios['grave'])}",
                 async_mode=True)
        else:
            pass

        if self.wpm > 100:
            play(f"res/{self.flavour}/speed/{choice(listdir('res/light/speed'))}")

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
                self.incorrect_seq = 0
                return (self.index == self.content_length, c)
            else:
                self.incorrect_entries += 1
                self.incorrect_seq += 1
                self.__comment_on_error__()
                return (self.index == self.content_length, Fore.RED + c + Fore.RESET)

    def stats(self) -> (int, int):
        self.__update__()
        return (round(self.wpm), round(self.accuracy * 100))


# Press and release event actions.
content_file = "res/content.yaml"
print(Fore.MAGENTA + "MANGLISH ACHEZHUTHU PARISHEELANA SHALA" + Fore.RESET + "\n")
with open(content_file) as f:
    content = safe_load(f.read())
    content = content['simple']
    content = choice(content)
    print(f"{content['work']} by {content['author']}")
    txt = content['content']
    txt = "\n\t" + txt.replace("\n", "\n\t")
    print(txt)

checker = Checker(content['content'])

def on_press(key):
    is_finished, key = checker.check(key)
    print(key, end='', flush=True)

    if is_finished:
        print(Fore.BLUE + "\nTest Complete" + Fore.RESET)
        wpm, accuracy = checker.stats()
        print(f"WPM: {wpm}\nAccuracy: {accuracy}%")

        if wpm >= 50 and accuracy > 90:
            play(f"res/light/appreciation/{choice(listdir('res/light/appreciation'))}")
            print(Fore.GREEN + "Kollaam!" + Fore.RESET)
        
        stop_listening()


def on_release(key):
    pass

# Here follows the start of execution.
def main() -> None:
    try:
        listen_keyboard(
                on_press=on_press,
                on_release=on_release,
                delay_second_char=0.1)
    except KeyboardInterrupt:
        if checker.index > 10:
            play("res/light/quit/ramankutty.mp3")
        exit(0);


if __name__ == "__main__":
    main()
