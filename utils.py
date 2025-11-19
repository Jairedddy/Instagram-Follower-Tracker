import sys
import re
try:
    import msvcrt  
    WINDOWS = True
except ImportError:
    import termios
    import tty
    WINDOWS = False

from selenium.webdriver.common.keys import Keys


def parse_count(text):
    if not text:
        return 0
    text = text.replace(',', '').strip()
    if 'K' in text.upper():
        return int(float(text.upper().replace('K', '')) * 1000)
    elif 'M' in text.upper():
        return int(float(text.upper().replace('M', '')) * 1000000)
    try:
        return int(text)
    except ValueError:
        return 0


def update_progress_bar(current, total, scroll_count=0, bar_length=20):
    if total and total > 0:
        percent = min(current / total, 1.0)
    else:
        percent = 0.5
    
    filled = int(bar_length * percent)
    bar = '#' * filled + '-' * (bar_length - filled)
    percent_str = f"{int(percent * 100)}%"
    if total:
        print(f"\r({bar}) {percent_str} accounts loaded ({current} out of {total}). Scroll: {scroll_count}", end='', flush=True)
    else:
        print(f"\r({bar}) {percent_str} accounts loaded ({current}). Scroll: {scroll_count}", end='', flush=True)


def input_to_browser_real_time(driver, element, prompt, is_password=False):
    print(prompt, end='', flush=True)
    input_text = ''
    
    if WINDOWS:
        while True:
            char = msvcrt.getch()
            if char == b'\r':
                print()
                break
            elif char == b'\x08':  
                if len(input_text) > 0:
                    input_text = input_text[:-1]
                    print('\b \b', end='', flush=True)
                    element.send_keys(Keys.BACKSPACE)
            else:
                try:
                    char_str = char.decode('utf-8')
                    input_text += char_str
                    display_char = '*' if is_password else char_str
                    print(display_char, end='', flush=True)
                    element.send_keys(char_str)
                except UnicodeDecodeError:
                    pass
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                char = sys.stdin.read(1)
                if char == '\r' or char == '\n':
                    print()  # New line
                    break
                elif char == '\x7f' or char == '\b':
                    if len(input_text) > 0:
                        input_text = input_text[:-1]
                        print('\b \b', end='', flush=True)
                        element.send_keys(Keys.BACKSPACE)
                else:
                    input_text += char
                    display_char = '*' if is_password else char
                    print(display_char, end='', flush=True)
                    element.send_keys(char)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    return input_text