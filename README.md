# Flutter Forge - Automated Flutter App Build and Rename Tool

**Flutter Forge** is an automated tool designed to simplify and streamline the process of building and renaming Flutter apps. This script provides a seamless solution for automating app versioning, building APKs, and renaming APK files, making it easy for developers to manage Flutter builds efficiently.

---

## Features

- **Automated Flutter Build**: Automatically builds Flutter APKs with `flutter build apk` commands.
- **APK Renaming**: Renames the APK files based on the app name and version.
- **Clean Build Option**: Supports running `flutter clean` to remove old builds and ensure fresh builds.
- **Customizable App Name and Version**: Allows customization of the app name and version during the build process.
- **Error Handling with Traceback**: Provides detailed error tracebacks for troubleshooting.
- **Cross-Platform Support**: Works on both Windows and Unix-based systems.

---

## Installation

### Prerequisites

1. **Flutter SDK**: Ensure that Flutter is installed and configured on your machine. You can install Flutter by following the official instructions [here](https://flutter.dev/docs/get-started/install).
   
2. **Python**: This script requires Python 3.x. Ensure that Python is installed on your machine. Download it from [here](https://www.python.org/downloads/).

3. **Required Python Libraries**:
   Install the required Python libraries by running:
   ```bash
   pip install colorama termcolor
   ```

---

## Usage

### Command-Line Arguments

The script accepts several command-line arguments to control its behavior. Below are the available options:

- `--build`: Initiates the build process. This is the main argument to start the APK build and renaming.
- `--traceback`: Enables detailed error traceback. Useful for debugging errors during execution.
- `--app-name <name>`: Allows you to specify a custom app name instead of using the default detected name.
- `--app-version <version>`: Allows you to specify a custom app version instead of using the default version detected from `pubspec.yaml`.
- `--clean-build`: If enabled, runs `flutter clean` before building the APKs to ensure a fresh build.

---

### Example Usage

Below are various ways you can use the script with different arguments:

1. **Basic Build (with default settings):**
   ```bash
   python script.py --build
   ```

2. **Build with Custom App Name:**
   Specify a custom app name.
   ```bash
   python script.py --build --app-name "MyApp"
   ```

3. **Build with Custom App Version:**
   Specify a custom app version.
   ```bash
   python script.py --build --app-version "v2.0.0"
   ```

4. **Build with Flutter Clean:**
   Run `flutter clean` before building.
   ```bash
   python script.py --build --clean-build
   ```

5. **Build with Custom App Name and Version:**
   Specify both custom app name and version.
   ```bash
   python script.py --build --app-name "MyApp" --app-version "v1.0.0"
   ```

6. **Build with Traceback (for detailed error output):**
   Enable traceback for detailed error logs.
   ```bash
   python script.py --build --traceback
   ```

7. **Build with Custom App Name, Version, and Clean:**
   Combine custom app name, version, and cleaning before building.
   ```bash
   python script.py --build --app-name "MyApp" --app-version "v3.1.0" --clean-build
   ```

8. **Build with All Options:**
   Specify all options including custom app name, version, cleaning, and traceback.
   ```bash
   python script.py --build --app-name "MyApp" --app-version "v4.0.0" --clean-build --traceback
   ```

---

## Error Handling

In case of an error, the script will display an appropriate message and can show a detailed traceback if the `--traceback` argument is used. Common errors include missing files or directories, such as the `pubspec.yaml` file or the APK directory.

---