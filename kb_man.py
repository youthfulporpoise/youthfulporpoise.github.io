from sshkeyboard import listen_keyboard

key_repr = {
    "space": " ",
    "backspace": "\b",
    "tab": "\t",
    "enter": "\n"
}

def on_press(key):
    k = key_repr.get(key, key)
    if k == "\b":
        print(f"\b \b", end='', flush=True)
    else:
        print(k, end='', flush=True)

def on_release(key):
    pass

# Here follows the start of execution.
try:
    listen_keyboard(
            on_press=on_press,
            on_release=on_release,
            delay_second_char=0.1
    )
except KeyboardInterrupt:
    print("\nQuitting ...")
    exit(0);
