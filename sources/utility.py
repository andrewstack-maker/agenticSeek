
from colorama import Fore
from termcolor import colored
import platform
import threading
import itertools
import time

global thinking_toggle
thinking_toggle = False

def get_color_map():
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
    else:
        color_map = {
            "success": "green",
            "failure": "red",
            "status": "light_green",
            "code": "light_blue",
            "warning": "yellow",
            "output": "cyan",
            "info": "black"
        }
    return color_map

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
    global thinking_toggle
    thinking_toggle = False
    color_map = get_color_map()
    if color not in color_map:
        color = "info"
    print(colored(text, color_map[color]))
    print(' ' * 10) # prevent cut-off

def animate_thinking(text, color="status", duration=30):
    """
    Animate a thinking spinner while a task is being executed.
    It use a daemon thread to run the animation. This will not block the main thread.
    Color are the same as pretty_print.
    """
    global thinking_toggle
    thinking_toggle = False
    def _animate():
        global thinking_toggle
        color_map = get_color_map()
        fore_color, term_color = color_map.get(color, color_map["info"])
        #spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        spinner = itertools.cycle([
            '█▒▒▒▒▒', '██▒▒▒▒', '███▒▒▒', '████▒▒', '█████▒', '██████',  
            '█████▒', '████▒▒', '███▒▒▒', '██▒▒▒▒', '█▒▒▒▒▒', '▒█▒▒▒█',
            '▒▒█▒█▒', '▒▒▒██▒', '▒█▒█▒▒', '█▒▒▒▒▒'
        ])
        end_time = time.time() + duration

        while time.time() < end_time:
            if not thinking_toggle:
                # stop if another text is printed
                break
            symbol = next(spinner)
            if platform.system().lower() != "windows":
                print(f"{fore_color}{symbol} {text}{Fore.RESET}", flush=True)
            else:
                print(colored(f"{symbol} {text}", term_color), flush=True)
            time.sleep(0.1)
            print("\033[1A\033[K", end="", flush=True)
    thinking_toggle = True
    animation_thread = threading.Thread(target=_animate, daemon=True)
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
        pretty_print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute", "status")
        return result
    return wrapper