import urllib
import urllib.request
import json
import pathlib
import os

def getNewVersion() -> tuple[str, str]:
    """_summary_

    Raises:
        ValueError: _description_

    Returns:
        tuple[str, str]: version, publishedAt
    """
    releaseURL = "https://api.github.com/repos/zen-browser/desktop/releases/latest"

    response = urllib.request.urlopen(url=releaseURL)

    data = json.loads(response.read())

    version = data["tag_name"]
    publishedAt = data["published_at"]
    
    if not version or not publishedAt:
        raise ValueError("Could not get version or publishedAt")
    
    return version, publishedAt

def getCurrentVersion():
    versionPath = pathlib.Path("version")
    versionPath.touch()
    versionFile = open(file=versionPath, mode="r")
    version = versionFile.read().strip()
    versionFile.close()
    return version

def isVersionUpToDate(newVersion: str) -> bool:
    currentVersion = getCurrentVersion()
    return currentVersion == newVersion

def updateVersion(newVersion: str):
    versionPath = pathlib.Path("version")
    versionFile = open(file=versionPath, mode="w")
    versionFile.write(newVersion)
    versionFile.close()

def githubOutput(version: str, update: bool):
    githubPath = pathlib.Path(os.getenv('GITHUB_OUTPUT'))
    githubPath.touch()
    
    up = "true" if update else "false"
    
    with open(file=githubPath, mode="w") as file:
        file.write(f"update={up}\nversion={version}")
    

if __name__ == "__main__":
    version, publishedAt = getNewVersion()
    if not isVersionUpToDate(version):
        updateVersion(version)
        githubOutput(version, True)
    else: 
        githubOutput(version, False)
        