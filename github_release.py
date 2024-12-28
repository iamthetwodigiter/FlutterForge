import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from common import colored_text

class GitHub:
    def __init__(self, dotenv_path=".env"):

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
        self.ASSET_FILES = ["flutterforge.exe"]

    def git_config(self) -> list:
        """Fetches the repository info from the .git/config file."""
        git_config_path = Path.cwd() / '.git' / 'config'

        if git_config_path.exists():
            with open(git_config_path, "r") as file:
                for line in file:
                    if 'url' in line:
                        url = line.strip().split("/")
                        owner = url[-2]
                        name = url[-1].replace(".git", "")
                        return [owner, name]
        else:
            raise ValueError(".git/config file not found.")

    def get_repo_from_env(self) -> tuple:
        """Fetches repository info from environment variables."""
        repo_owner = os.getenv("REPO_OWNER")
        repo_name = os.getenv("REPO_NAME")
        if not repo_owner or not repo_name:
            raise ValueError("REPO_OWNER or REPO_NAME is missing in the environment variables.")
        return repo_owner, repo_name

    def create_release(self):
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
            colored_text("Release created successfully!")
            release = response.json()
            return release["upload_url"].split("{")[0]
        else:
            raise ValueError(f"Failed to create release: {response.status_code}, {response.text}")

    def upload_asset(self, upload_url, file_path):
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
                colored_text(f"Uploaded asset: {file_name}")
            else:
                raise ValueError(f"Failed to upload asset {file_name}: {response.status_code}, {response.text}")

def release():
    try:
        github = GitHub()
        colored_text("CREATING GITHUB RELEASE")
        upload_url = github.create_release()
        if upload_url:
            for asset in github.ASSET_FILES:
                asset_path = os.path.join(os.getcwd(), asset)  
                if os.path.exists(asset_path):
                    colored_text("UPLOADING ASSETS")
                    github.upload_asset(upload_url, asset_path)
                else:
                    raise ValueError(f"Asset not found: {asset_path}")

    except Exception as e:
        colored_text(f"\nERROR: {type(e).__name__}: {e}\n", color="red")