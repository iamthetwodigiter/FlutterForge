import os
from colorama import just_fix_windows_console
from termcolor import colored
import subprocess

# GLOBAL FUNCTIONS
def clear() -> None:
    """Clears the terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def take_input(prompt: str) -> str:
    """Takes user input with a prompt."""
    print("=" * 40)
    return input(prompt)


def colored_text(
    text: str, color="blue", on_color=None, text_2="", color_2=None, on_color_2=None
) -> None:
    """Prints colored text."""
    just_fix_windows_console()
    print(
        colored(text, color, on_color, ["bold"])
        + colored(text_2, color_2, on_color_2, ["bold"]),
        end="",
        flush=True,
    )

def run_command(command: list, description: str = "") -> None:
    """Runs a shell command and handles errors."""
    try:
        colored_text(f"\n{description}\n")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {' '.join(command)} | Error: {e}")