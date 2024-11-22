from pygame import mixer
from sshkeyboard import listen_keyboard, stop_listening
from colorama import *
from time import time
from os import listdir
from random import choice
from yaml import safe_load

class Checker:
    '''This class loads the content to be transcribed and checks the inputs of
    the user.'''

    content: str = ""
    content_length: int = 0
    index: int = 0
    key_repr: {str, str} = {
        "space": " ",
        "backspace": "\b",
        "tab": "\t",
        "enter": "\n"
    }

    intervals: [int] = []  # stores time intervals between key presses
    wpm: float = 0  # stores WPM

    incorrect_seq: int = 0  # counts the number mistakes the user makes sequentially
    incorrect_entries: int = 0
    correct_entries: int = 0
    accuracy: int = 0  # stores typing accuracy in percentage

    flavour: str
    audios: {str, str}
    sound: str

    def __init__(self, content, flavour="light"):
        self.content = content
        self.content_length = len(content)

        self.flavour = flavour
        self.audios = {
                -2: f"res/{self.flavour}/speed",
                -1: f"res/{self.flavour}/appreciation",
                 0: f"res/{self.flavour}/error/s1",
                 1: f"res/{self.flavour}/error/s2",
                 2: f"res/{self.flavour}/error/s3"
        }

        mixer.init()

    def __next__(self) -> str:
        if (self.index < self.content_length):
            s = self.content[self.index]
            self.index += 1
        else: pass
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

    def __comment_on_error__(self) -> None:
        if self.incorrect_seq == 1: self.__play_sound__(0)
        elif 1 < self.incorrect_seq < 3: self.__play_sound__(1)
        elif 3 < self.incorrect_seq < 5: self.__play_sound__(2)
        else: pass

        if self.wpm > 100: self.__play_sound__(-2)

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

    def __play_sound__(self, gravity: int) -> str:
        bucket: str = self.audios[gravity]
        audio: str = bucket + '/' + choice(listdir(bucket))

        mixer.stop()
        self.sound = mixer.Sound(audio)
        self.sound.play()



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

checker = Checker(content['content'].strip())

def on_press(key):
    is_finished, key = checker.check(key)
    print(key, end='', flush=True)

    if is_finished:
        print(Fore.BLUE + "\n\nTest Complete" + Fore.RESET)
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
            mixer.Sound("res/light/quit/ramankutty.mp3").play()
        exit(0);


if __name__ == "__main__":
    main()
