
import os

set_color = os.getenv("TERM") == "xterm-256color"

def try_change_font_of_string(color_num, s):
    return "\033[" + color_num + "m" + s + "\033[m" if set_color else s

