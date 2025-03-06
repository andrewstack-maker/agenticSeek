
from colorama import Fore
from termcolor import colored
import platform


def pretty_print(text, color = "info"):
    """
    Print text with color formatting.

    Args:
        text (str): The text to print
        color (str, optional): The color to use. Defaults to "info".
            Valid colors are:
            - "success": Green
            - "failure": Red 
            - "status": Light green
            - "code": Light blue
            - "warning": Yellow
            - "output": Cyan
            - "default": Black (Windows only)
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

def timer_decorator(func):
    """
    Decorator to measure the execution time of a function.
    Usage:
    @timer_decorator
    def my_function():
        # code to execute
    """
    from time import time
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute")
        return result
    return wrapper