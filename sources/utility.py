
from colorama import Fore
from termcolor import colored
import platform
import threading
import itertools
import time


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
            "info": Fore.CYAN
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
            "warning": "yellow",
            "output": "cyan",
            "default": "black"
        }
        if color not in color_map:
            color = "default"
        print(colored(text, color_map[color]))

def animate_thinking(text, color="status", duration=2):
    """
    Display an animated "thinking..." indicator in a separate thread.
    Args:
        text (str): Text to display
        color (str): Color for the text
        duration (float): How long to animate in seconds
    """
    def _animate():
        color_map = {
            "success": (Fore.GREEN, "green"),
            "failure": (Fore.RED, "red"),
            "status": (Fore.LIGHTGREEN_EX, "light_green"),
            "code": (Fore.LIGHTBLUE_EX, "light_blue"),
            "warning": (Fore.YELLOW, "yellow"),
            "output": (Fore.LIGHTCYAN_EX, "cyan"),
            "default": (Fore.RESET, "black"),
            "info": (Fore.CYAN, "cyan")
        }

        fore_color, term_color = color_map[color]
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        end_time = time.time() + duration

        while time.time() < end_time:
            symbol = next(spinner)
            if platform.system().lower() != "windows":
                print(f"\r{fore_color}{symbol} {text}{Fore.RESET}", end="", flush=True)
            else:
                print(colored(f"\r{symbol} {text}", term_color), end="", flush=True)
            time.sleep(0.1)
        print()
    animation_thread = threading.Thread(target=_animate)
    animation_thread.daemon = True
    animation_thread.start()

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