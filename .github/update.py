from version import isVersionUpToDate, getNewVersion, updateVersion
from generateFlake import generateFlake
def update():
    newVersion, publishedAt = getNewVersion()
    
    print(f"Updating to: {newVersion} ({publishedAt})")
    
    # UPDATE FLAKE
    print("generating flake.nix file...")
    generateFlake(version=newVersion)
    
    print("updated flake.nix file")
    
if __name__ == "__main__":
    update()