
from colorama import Fore
from termcolor import colored
import platform


def pretty_print(text, color = "info"):
    """
    print text with color
    """
    if platform.system().lower() != "windows":
        color_map = {
            "success": Fore.GREEN,
            "failure": Fore.RED,
            "status": Fore.LIGHTGREEN_EX,
            "code": Fore.LIGHTBLUE_EX,
            "warning": Fore.YELLOW,
            "output": Fore.LIGHTCYAN_EX,
        }
        if color not in color_map:
            print(text)
            pretty_print(f"Invalid color {color} in pretty_print", "warning")
            return
        print(color_map[color], text, Fore.RESET)
    else:
        color_map = {
            "success": "green",
            "failure": "red",
            "status": "light_green",
            "code": "light_blue",
            "warning": "yello",
            "output": "cyan",
            "default": "black"
        }
        if color not in color_map:
            color = "default"
        print(colored(text, color_map[color]))
