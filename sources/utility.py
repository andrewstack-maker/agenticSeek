
from colorama import Fore
from termcolor import colored
import platform
import threading
import itertools
import time

def pretty_print(text, color="info"):
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
        print(f"{color_map[color]}{text}{Fore.RESET}")
        print(' ' * 10) # prevent cut-off
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
        print(' ' * 10) # prevent cut-off

def animate_thinking(text, color="status", duration=2):
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
        fore_color, term_color = color_map.get(color, color_map["default"])
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        end_time = time.time() + duration

        while time.time() < end_time:
            symbol = next(spinner)
            if platform.system().lower() != "windows":
                print(f"{fore_color}{symbol} {text}{Fore.RESET}", flush=True)
            else:
                print(colored(f"{symbol} {text}", term_color), flush=True)
            time.sleep(0.1)
            print("\033[1A\033[K", end="", flush=True)
    animation_thread = threading.Thread(target=_animate)
    animation_thread.start()
    animation_thread.join()

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
        pretty_print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute", "status")
        return result
    return wrapper