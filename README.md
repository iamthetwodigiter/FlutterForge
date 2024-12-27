# Flutter Forge - Automated Flutter App Build and Rename Tool

**Flutter Forge** is an automated tool designed to simplify and streamline the process of building and renaming Flutter apps. This script provides a seamless solution for automating app versioning, building APKs, and renaming APK files, making it easy for developers to manage Flutter builds efficiently.

---

## Features

- **Automated Flutter Build**: Automatically builds Flutter APKs with `flutter build apk` commands.
- **Universal APK Build**: Supports building universal APKs for all target architectures with the `--universal-build` option.
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

4. **(Optional) Flutter Forge Executable**: If you want to use the `.exe` version (for Windows), download the executable and add it to your system's environment variables for easier access.

---

## Usage

### Command-Line Arguments

The script and executable accept the same command-line arguments to control their behavior. Below are the available options:

- `--build`: Initiates the build process. This is the main argument to start the APK build and renaming.
- `--universal-build`: Builds a universal APK for all target architectures.
- `--traceback`: Enables detailed error traceback. Useful for debugging errors during execution.
- `--app-name <name>`: Allows you to specify a custom app name instead of using the default detected name.
- `--app-version <version>`: Allows you to specify a custom app version instead of using the default version detected from `pubspec.yaml`.
- `--clean-build`: If enabled, runs `flutter clean` before building the APKs to ensure a fresh build.

---

### Example Usage

You have two options for running the tool: using the **Python script** or the **compiled `.exe` file**.

<details>
<summary><strong>Using the Python Script</strong></summary>

1. **Basic Build (with default settings):**
   ```bash
   python script.py --build
   ```

2. **Universal Build:**
   Create a universal APK.
   ```bash
   python script.py --universal-build
   ```

3. **Build with Custom App Name:**
   Specify a custom app name.
   ```bash
   python script.py --build --app-name "MyApp"
   ```

4. **Build with Custom App Version:**
   Specify a custom app version.
   ```bash
   python script.py --build --app-version "v2.0.0"
   ```

5. **Build with Flutter Clean:**
   Run `flutter clean` before building.
   ```bash
   python script.py --build --clean-build
   ```

6. **Universal Build with Custom App Name:**
   Specify a custom app name while building a universal APK.
   ```bash
   python script.py --universal-build --app-name "MyApp"
   ```

7. **Build with Traceback (for detailed error output):**
   Enable traceback for detailed error logs.
   ```bash
   python script.py --build --traceback
   ```

8. **Build with All Options:**
   Specify all options including custom app name, version, cleaning, and traceback.
   ```bash
   python script.py --build --app-name "MyApp" --app-version "v4.0.0" --clean-build --traceback
   ```

</details>

<details>
<summary><strong>Using the `.exe` File</strong></summary>

1. **Basic Build (with default settings):**
   Ensure the `.exe` is added to your system's environment variables, then run:
   ```bash
   flutterforge.exe --build
   ```

2. **Universal Build:**
   Create a universal APK.
   ```bash
   flutterforge.exe --universal-build
   ```

3. **Build with Custom App Name:**
   Specify a custom app name.
   ```bash
   flutterforge.exe --build --app-name "MyApp"
   ```

4. **Build with Custom App Version:**
   Specify a custom app version.
   ```bash
   flutterforge.exe --build --app-version "v2.0.0"
   ```

5. **Build with Flutter Clean:**
   Run `flutter clean` before building.
   ```bash
   flutterforge.exe --build --clean-build
   ```

6. **Universal Build with Custom App Name:**
   Specify a custom app name while building a universal APK.
   ```bash
   flutterforge.exe --universal-build --app-name "MyApp"
   ```

7. **Build with Traceback (for detailed error output):**
   Enable traceback for detailed error logs.
   ```bash
   flutterforge.exe --build --traceback
   ```

8. **Build with All Options:**
   Specify all options including custom app name, version, cleaning, and traceback.
   ```bash
   flutterforge.exe --build --app-name "MyApp" --app-version "v4.0.0" --clean-build --traceback
   ```

</details>

---

## Error Handling

In case of an error, the script will display an appropriate message and can show a detailed traceback if the `--traceback` argument is used. Common errors include missing files or directories, such as the `pubspec.yaml` file or the APK directory.

---