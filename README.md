# Flutter Forge - Automated Flutter App Build and Rename Tool

**Flutter Forge** is an automated tool designed to simplify and streamline the process of building and renaming Flutter apps. This script provides a seamless solution for automating app versioning, building APKs, and renaming APK files, making it easy for developers to manage Flutter builds efficiently.

---

## Features

- **Automated Flutter Build**: Automatically builds Flutter APKs with `flutter build apk` commands.
- **Universal APK Build**: Supports building universal APKs for all target architectures with the `--universal-build` option.
- **APK Renaming**: Renames the APK files based on the app name and version.
- **Clean Build Option**: Supports running `flutter clean` to remove old builds and ensure fresh builds.
- **Customizable App Name and Version**: Allows customization of the app name and version during the build process.
- **GitHub Release**: Allows assets to be uploaded to GitHub creating a new release with desired tag, title and description.
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
   pip install -r requirements.txt
   ```

4. **env**: Create `.env` file inside project directory with the following data

```
REPO_OWNER=YOUR_GITHUB_USERNAME
REPO_NAME=YOUR_REPO_NAME
GITHUB_TOKEN=YOUR_GITHUB_TOKEN

TAG_NAME=RELEASE_TAG
RELEASE_NAME=RELEASE_TITLE
RELEASE_BODY=RELEASE_DESCRIPTION [Supports multiline description with \n]
```

5. **(Optional but Recommended) Flutter Forge Executable**: If you want to use the `.exe` version (for Windows), download the executable and add it to your system's environment variables for easier access.

---

## Usage

### Command-Line Arguments

- `--build`: Initiates the build process, including APK creation and renaming.
- `--universal-build`: Builds a universal APK that supports all target architectures.
- `--traceback`: Enables detailed error traceback for debugging.
- `--app-name <name>`: Specifies a custom app name instead of using the default detected name.
- `--app-version <version>`: Specifies a custom app version instead of using the version from `pubspec.yaml`.
- `--clean-build`: Runs `flutter clean` before building, ensuring a fresh build.
- `--release`: Starts the GitHub release process for the app, creating a new release on GitHub.

---

### Example Usage

<details>
<summary><strong>Using the Python Script</strong></summary>

1. **Basic Build (with default settings):**
   ```bash
   python main.py --build
   ```

2. **Universal Build:**
   Build a universal APK.
   ```bash
   python main.py --universal-build
   ```

3. **Start GitHub Release Process:**
   This command triggers the process to create a GitHub release and upload the APK to the release assets.
   > The apk files should be present inside the default folder for standalone release command to work without build command
   ```bash
   python main.py --release
   ```

4. **Build with Custom App Name:**
   Specify a custom app name.
   ```bash
   python main.py --build --app-name "MyApp"
   ```

5. **Build with Custom App Version:**
   Specify a custom app version.
   ```bash
   python main.py --build --app-version "v2.0.0"
   ```

6. **Build with Flutter Clean:**
   Run `flutter clean` before building.
   ```bash
   python main.py --build --clean-build
   ```

7. **Universal Build with Custom App Name:**
   Build a universal APK with a custom app name.
   ```bash
   python main.py --universal-build --app-name "MyApp"
   ```

8. **Build with Traceback (for detailed error output):**
   Enable traceback for detailed error logs.
   ```bash
   python main.py --build --traceback
   ```

9. **Start GitHub Release Process with All Options:**
   Trigger the GitHub release process, with custom app name, version, cleaning, and traceback.
   ```bash
   python main.py --build --universal-build --release --app-name "MyApp" --app-version "v4.0.0" --clean-build --traceback
   ```

</details>

<details>
<summary><strong>Using the `.exe` File</strong></summary>

1. **Start GitHub Release Process:**
   This command triggers the GitHub release process, creating a new release and uploading the APK to the release assets.
   ```bash
   flutterforge.exe --release
   ```

2. **Universal Build:**
   Build a universal APK.
   ```bash
   flutterforge.exe --universal-build
   ```

3. **Start GitHub Release Process:**
   This command triggers the process to create a GitHub release and upload the APK to the release assets.
   > The apk files should be present inside the default folder for standalone release command to work without build command
   ```bash
   flutterforge.exe --release
   ```

4. **Build with Custom App Name:**
   Specify a custom app name.
   ```bash
   flutterforge.exe --build --app-name "MyApp"
   ```

5. **Build with Custom App Version:**
   Specify a custom app version.
   ```bash
   flutterforge.exe --build --app-version "v2.0.0"
   ```

6. **Build with Flutter Clean:**
   Run `flutter clean` before building.
   ```bash
   flutterforge.exe --build --clean-build
   ```

7. **Universal Build with Custom App Name:**
   Build a universal APK with a custom app name.
   ```bash
   flutterforge.exe --universal-build --app-name "MyApp"
   ```

8. **Build with Traceback (for detailed error output):**
   Enable traceback for detailed error logs.
   ```bash
   flutterforge.exe --build --traceback
   ```

9. **Start GitHub Release Process with All Options:**
   Trigger the GitHub release process, with custom app name, version, cleaning, and traceback.
   ```bash
   flutterforge.exe --build --universal-build --release --app-name "MyApp" --app-version "v4.0.0" --clean-build --traceback
   ```

</details>

---

### GitHub Release Process

The `--release` command will initiate the GitHub release process by:

1. **Creating a GitHub release**: It automatically creates a release on GitHub.
2. **Uploading APKs**: It uploads the newly built APKs to the release assets.

To ensure this works, you'll need to have GitHub credentials stored in your environment variables for the tool to authenticate and push the release.

---

## GitHub Release Automation

This tool automates the process of creating a release on GitHub and uploading assets (e.g., APK files or executables) to the release.

### Prerequisites:
- **Git Repository**: The project folder must have a Git repository initialized for better functionality.
- **.env Configuration**: Ensure that the `.env` file is set up with your GitHub repository details and Access Token for authentication.
  
### How It Works:
1. **Configuration Check**: The script first checks for the `.git/config` file in the project directory to automatically retrieve the repository details. If not found, it falls back to values provided in the `.env` file.
2. **Create Release**: Using GitHub's REST API, the script creates a release with the specified version, release notes, and other metadata.
3. **Upload Assets**: After creating the release, the script uploads specified assets (such as APKs or executables) to the release.

The entire process is encapsulated within a class for better code reusability and organization.

### How to Use:
1. **Set Up**: Configure the `.env` file with the necessary details (GitHub Token, Repository Owner, Repository Name, etc.).
2. **Run the Release**: Execute the release script to create a GitHub release and upload the assets:
   ```bash
   python main.py --release
   ```

---

## Error Handling

In case of an error, the script will display an appropriate message and can show a detailed traceback if the `--traceback` argument is used. Common errors include missing files or directories, such as the `pubspec.yaml` file, `.env` file or the APK directory.

---