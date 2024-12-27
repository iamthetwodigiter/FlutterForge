import os
import subprocess
from pathlib import Path
from colorama import just_fix_windows_console
from termcolor import colored
import re
import argparse
import traceback


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


def find_version() -> str:
    """Finds the app version from pubspec.yaml."""
    pubspec_path = Path.cwd() / "pubspec.yaml"
    if pubspec_path.exists():
        with open(pubspec_path, "r") as file:
            for line in file:
                if line.strip().startswith("version:"):
                    match = re.match(r"version:\s*(\S+)", line)
                    if match:
                        return match.group(1)
    raise FileNotFoundError("pubspec.yaml not found or version not defined.")


def run_command(command: list, description: str = "") -> None:
    """Runs a shell command and handles errors."""
    try:
        colored_text(f"\n{description}\n")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {' '.join(command)} | Error: {e}")


def rename_apks(apk_dir: Path, app_name: str, app_version: str) -> None:
    """Renames APK files in the specified directory."""
    for file in apk_dir.glob("*.apk"):
        if file.name == "app-debug.apk":
            continue
        if file.name == "app-release.apk":
            new_name = f"{app_name}-{app_version}-universal.apk"
        else:
            new_name = file.name.replace("app", f"{app_name}-{app_version}").replace(
                "-release", ""
            )
        file.rename(apk_dir / new_name)
    colored_text(
        f"\nAPKS RENAMED SUCCESSFULLY\nAPPS CAN BE FOUND IN {apk_dir}\n", color="green"
    )


# MAIN FUNCTION
def main(args):
    colored_text(
        "\nWelcome to Flutter Forge - an automated tool to build and rename Flutter apps by thetwodigiter❤️\n",
        color="magenta",
    )

    try:
        # CONSTANTS
        current_dir = Path.cwd()
        extracted_app_name = current_dir.name.capitalize()
        apk_dir = current_dir / "build/app/outputs/flutter-apk"
        flutter_cmd = "C://flutter/bin/flutter.bat"

        # APP NAME
        colored_text(
            "\nDETECTED APP NAME => ", text_2=f"{extracted_app_name}\n", color_2="green"
        )
        app_name = (
            args.app_name
            or take_input(
                "Do you want to keep the name or change it?\n[Leave it empty to use the detected name]: "
            )
            or extracted_app_name
        )

        # APP VERSION
        app_version = f"v{find_version()}"
        colored_text(
            "\nDETECTED APP VERSION => ", text_2=f"{app_version}\n", color_2="green"
        )
        app_version = (
            args.app_version
            or take_input(
                "Do you want to keep the version or change it?\n[Leave it empty to use the detected version]: "
            )
            or app_version
        )

        # CLEAN BUILD
        clean_build = (
            args.clean_build
            or take_input(
                "Run flutter clean? [Delete old builds]\n[Y or N, Leave empty for No]: "
            ).lower()
            == "y"
        )
        if clean_build:
            run_command([flutter_cmd, "clean"], description="CLEANING THE BUILD FOLDER")
            run_command(
                [flutter_cmd, "pub", "get"],
                description="RUNNING 'flutter pub get' TO DOWNLOAD ALL DEPENDENCIES",
            )

        # BUILD THE APPS
        run_command(
            [flutter_cmd, "build", "apk", "--split-per-abi", "--release"],
            description="BUILDING THE APPS [SPLIT PER ARCHITECTURE]",
        )
        if args.universal_build:
            run_command(
                [flutter_cmd, "build", "apk", "--release"],
                description="BUILDING THE UNIVERSAL APP",
            )

        # RENAME THE APKS
        if apk_dir.exists():
            rename_apks(apk_dir, app_name, app_version)
        else:
            raise FileNotFoundError(f"APK directory not found: {apk_dir}")

    except Exception as e:
        if args.traceback:
            traceback.print_exc()
        else:
            colored_text(f"\nERROR: {type(e).__name__}: {e}\n", color="red")


# ARGUMENT PARSER
def parse_args():
    parser = argparse.ArgumentParser(
        description="Flutter App Build and Rename Automation Script"
    )
    parser.add_argument(
        "--build", action="store_true", help="Start the main build process"
    )
    parser.add_argument(
        "--traceback", action="store_true", help="Enable detailed error traceback"
    )
    parser.add_argument("--app-name", type=str, help="Specify the app name directly")
    parser.add_argument(
        "--app-version", type=str, help="Specify the app version directly"
    )
    parser.add_argument(
        "--clean-build",
        action="store_true",
        help="Enable 'flutter clean' before building",
    )
    parser.add_argument(
        "--universal-build", action="store_true", help="Build the universal apk"
    )
    return parser.parse_args()


# ENTRY POINT
if __name__ == "__main__":
    clear()
    args = parse_args()
    if args.build:
        main(args)
    else:
        colored_text(
            "\nUse '--build' to start the main build process.\n", color="yellow"
        )
