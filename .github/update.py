from version import isVersionUpToDate, getNewVersion, updateVersion
from generateFlake import generateFlake
def update():
    newVersion, publishedAt = getNewVersion()
    isUpToDate = isVersionUpToDate(newVersion)
    
    if isUpToDate:
        print(f"Zen Browser is up to date. Current version: {newVersion}")
        return
    
    print(f"New version available: {newVersion} ({publishedAt})")
    
    # UPDATE FLAKE
    generateFlake(version=newVersion)
    
    updateVersion(newVersion)
    
if __name__ == "__main__":
    update()