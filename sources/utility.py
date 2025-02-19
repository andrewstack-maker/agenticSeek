
from colorama import Fore

def pretty_print(text, color = "info"):
    """
    print text with color
    """
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
        pretty_print("Invalid color in pretty_print", "warning")
        return
    print(color_map[color], text, Fore.RESET)