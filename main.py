import os
from pathlib import Path
import re
import traceback
from colorama import just_fix_windows_console
from termcolor import colored
import subprocess
import requests
from dotenv import load_dotenv
import argparse

CURRENT_DIR = Path.cwd()
APK_DIR = CURRENT_DIR / "build/app/outputs/flutter-apk"
FLUTTER = "C://flutter/bin/flutter.bat"

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

def asset_files_list() -> list:
    asset_files = []
    for file in APK_DIR.glob("*.apk"):
        if file.name == "app-debug.apk":
            continue
        else:
            asset_files.append((f'{APK_DIR}\{file.name}'))
    return asset_files if len(asset_files) != 0 else ValueError("No asset files found to be released")

class Build:
    def __init__(self):        
        self.extracted_app_name = CURRENT_DIR.name.capitalize()
        
    def find_version(self) -> str:
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

    def rename_apks(self, app_name: str, app_version: str) -> None:
        """Renames APK files in the specified directory."""
        for file in APK_DIR.glob("*.apk"):
            if file.name == "app-debug.apk":
                continue
            if file.name == "app-release.apk":
                new_name = f"{app_name}-{app_version}-universal.apk"
            else:
                new_name = file.name.replace("app", f"{app_name}-{app_version}").replace(
                    "-release", ""
                )
            file.rename(APK_DIR / new_name)
        t = len(f"\nAPKS RENAMED SUCCESSFULLY\nAPPS CAN BE FOUND IN {APK_DIR}\n")
        colored_text("="*t+4, color="light_green")
        colored_text(
            f"\n| APKS RENAMED SUCCESSFULLY\nAPPS CAN BE FOUND IN {APK_DIR} |\n", color="light_green"
        )
        colored_text("="*t+4, color="light_green")

    # MAIN FUNCTION
    def build(self, args) -> list:
    
        # APP NAME
        colored_text(
            "\nDetected App Name => ", color="yellow", text_2=f"{self.extracted_app_name}\n", color_2="cyan"
        )
        app_name = (
            args.app_name
            or take_input(
                "Do you want to keep the name or change it?\n[Leave it empty to use the detected name]: "
            )
            or self.extracted_app_name
        )

        # APP VERSION
        app_version = f"v{self.find_version()}"
        colored_text(
            "\nDetected App Version => ", color="yellow",text_2=f"{app_version}\n", color_2="cyan"
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
            run_command([FLUTTER, "clean"], description="CLEANING THE BUILD FOLDER")
            run_command(
                [FLUTTER, "pub", "get"],
                description="RUNNING 'flutter pub get' TO DOWNLOAD ALL DEPENDENCIES",
            )

        # BUILD THE APPS
        run_command(
            [FLUTTER, "build", "apk", "--split-per-abi", "--release"],
            description="BUILDING THE APPS [SPLIT PER ARCHITECTURE]",
        )
        if args.universal_build:
            run_command(
                [FLUTTER, "build", "apk", "--release"],
                description="BUILDING THE UNIVERSAL APP",
            )

        # RENAME THE APKS
        if APK_DIR.exists():
            self.rename_apks(app_name, app_version)
            
        else:
            raise FileNotFoundError(f"APK directory not found: {APK_DIR}")

    

class GitHub:
    def __init__(self, asset_files, dotenv_path=CURRENT_DIR/".env") -> None:

        load_dotenv(dotenv_path=dotenv_path)
        if not (Path(dotenv_path).exists):
            raise ValueError(".env file not found")
        
        repo_info = self.git_config()  
        self.REPO_OWNER, self.REPO_NAME = repo_info if repo_info else self.get_repo_from_env()

        self.GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if not self.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN environment variable is missing.")

        self.TAG_NAME = os.getenv("TAG_NAME")
        self.RELEASE_NAME = os.getenv("RELEASE_NAME")
        self.RELEASE_BODY = os.getenv("RELEASE_BODY")
        self.IS_DRAFT = False
        self.IS_PRERELEASE = False
        self.GENERATE_RELEASE_NOTES = False
        self.ASSET_FILES = asset_files

        colored_text(text="\n\nDetected GitHub Repository => ", color="yellow", text_2=self.REPO_NAME, color_2="cyan")
        colored_text(text="\nDetected Tag => ", color="yellow", text_2=self.TAG_NAME, color_2="cyan")
        colored_text(text="\nDetected Release Name => ", color="yellow", text_2=self.RELEASE_NAME, color_2="cyan")
        colored_text(text="\nDetected Release Description => ", color="yellow", text_2=self.RELEASE_BODY, color_2="cyan")
        colored_text(text="\nDetected Assets =>\n", color="yellow", text_2="\n".join(self.ASSET_FILES), color_2="cyan")

    def git_config(self) -> list:
        """Fetches the repository info from the .git/config file."""
        git_config_path = CURRENT_DIR / '.git' / 'config'

        if git_config_path.exists():
            with open(git_config_path, "r") as file:
                for line in file:
                    if 'url' in line:
                        url = line.strip().split("/")
                        owner = url[-2]
                        name = url[-1].replace(".git", "")
                        return [owner, name]
        else:
            colored_text("\n.git/config file not found.", color="red")

    def get_repo_from_env(self) -> tuple:
        """Fetches repository info from environment variables."""
        repo_owner = os.getenv("REPO_OWNER")
        repo_name = os.getenv("REPO_NAME")
        if not repo_owner or not repo_name:
            raise ValueError("REPO_OWNER or REPO_NAME is missing in the environment variables.")
        return repo_owner, repo_name

    def create_release(self) -> None:
        """Creates a new release on GitHub."""
        url = f"https://api.github.com/repos/{self.REPO_OWNER}/{self.REPO_NAME}/releases"
        headers = {"Authorization": f"token {self.GITHUB_TOKEN}"}
        payload = {
            "tag_name": self.TAG_NAME,
            "name": self.RELEASE_NAME,
            "body": self.RELEASE_BODY,
            "draft": self.IS_DRAFT,
            "prerelease": self.IS_PRERELEASE,
            "generate_release_notes": self.GENERATE_RELEASE_NOTES,
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            colored_text("\nRelease created successfully!", color="light_green")
            release = response.json()
            return release["upload_url"].split("{")[0]
        else:
            raise ValueError(f"Failed to create release: {response.status_code}, {response.text}")

    def upload_asset(self, upload_url, file_path) -> None:
        """Uploads assets to GitHub release."""
        headers = {
            "Authorization": f"token {self.GITHUB_TOKEN}",
            "Content-Type": "application/octet-stream",
        }
        file_name = os.path.basename(file_path)
        params = {"name": file_name}

        with open(file_path, "rb") as file_data:
            response = requests.post(upload_url, headers=headers, params=params, data=file_data)
            if response.status_code == 201:
                colored_text(text=f"\nUploaded asset: ",color="yellow", text_2=file_name, color_2="cyan")
            else:
                raise ValueError(f"Failed to upload asset {file_name}: {response.status_code}, {response.text}")

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="FlutterForge - Build & Release Automation")
    parser.add_argument(
        "--build", action="store_true", help="Start the Flutter build process"
    )
    parser.add_argument(
        "--release", action="store_true", help="Start the GitHub release process"
    )
    parser.add_argument(
        "--traceback", action="store_true", help="Enable detailed error traceback"
    )
    parser.add_argument(
        "--app-name", type=str, help="Specify the app name directly for build"
    )
    parser.add_argument(
        "--app-version", type=str, help="Specify the app version directly for build"
    )
    parser.add_argument(
        "--clean-build",
        action="store_true",
        help="Enable 'flutter clean' before building",
    )
    parser.add_argument(
        "--universal-build", action="store_true", help="Build the universal APK"
    )
    return parser.parse_args()

def build(args) -> bool:
    try:
        build = Build()
        build.build(args=args)
        return True
    except Exception as e:
        if args.traceback:
            traceback.print_exc()
        else:
            colored_text(f"\nERROR: {type(e).__name__}: {e}\n", color="red")
        return False

def release(asset_files) -> None:
    try:
        github = GitHub(asset_files)
        colored_text("\n\nCREATING GITHUB RELEASE")
        upload_url = github.create_release()
        if upload_url:
            colored_text("\n\nUPLOADING ASSETS")
            for asset in github.ASSET_FILES:
                asset_path = os.path.join(os.getcwd(), asset)  
                if os.path.exists(asset_path):
                    github.upload_asset(upload_url, asset_path)
                else:
                    raise ValueError(f"Asset not found: {asset_path}")
        return True
    except Exception as e:
        colored_text(f"\nERROR: {type(e).__name__}: {e}\n", color="red")
        return False

def main():
    """Main function to control the flow of the build and release process."""
    args = parse_args()
    clear()
    colored_text(
            "\nWelcome to Flutter Forge - an automated tool to build and rename Flutter apps by thetwodigiter❤️\n",
            color="magenta",
        )
    if args.build:
        colored_text("="*32, color='cyan')
        colored_text("\n| Starting the build process.. |\n", color='cyan')
        colored_text("="*32, color='cyan')
        print()
        x = build(args)
    if args.release:
        asset_files = asset_files_list()
        colored_text("="*34, color='cyan')
        colored_text("\n| Starting the release process.. |\n", color='cyan')
        colored_text("="*34, color='cyan')
        print()
        y = release(asset_files=asset_files)

    if not args.build and not args.release:
        colored_text("No valid option provided. Please use --build or --release.", color='yellow')

    if x and y:
        colored_text("="*37, color='cyan')
        colored_text("\n| Process Completed Successfully... |\n", color='cyan')
        colored_text("="*37, color='cyan')
        print()

if __name__ == "__main__":
    main()