from pathlib import Path
import re
import traceback
from common import colored_text, take_input, run_command

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

