import argparse
from build import main as build_main
from github_release  import release
from common import colored_text, clear

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

def main():
    """Main function to control the flow of the build and release process."""
    args = parse_args()
    clear()
    if args.build:
        colored_text("Starting the build process...")
        build_main(args)
    elif args.release:
        colored_text("Starting the release process...")
        release()
    else:
        colored_text("No valid option provided. Please use --build or --release.", color='yellow')

if __name__ == "__main__":
    main()