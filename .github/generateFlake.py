import subprocess
import pathlib

def prefetch(url: str):
    print("Fetching URL:", url)
    
    res = subprocess.run(["nix-prefetch-url", f"{url}", "--unpack"], capture_output=True, text=True)
    
    print("Errors:", res.stderr, "\nSTDOUT:", res.stdout)
    
    return res.stdout.splitlines()[0].strip()

def getSHA256s(genericURL: str, specificURL: str):
    specificHASH = prefetch(url=specificURL)
    genericHASH = prefetch(url=genericURL)
    
    return specificHASH, genericHASH

def getTemplate():
    flakeTemplatePath = pathlib.Path("flake.nix.template")
    flakeTemplateFile = open(file=flakeTemplatePath, mode="r")
    flakeTemplate = flakeTemplateFile.read()
    return flakeTemplate


def generateFlakeContent(
    template: str, 
    version: str, 
    specificURL: str, 
    specificHASH: str, 
    genericURL: str, 
    genericHASH: str
    ):
    toReplace = {
        "{VERSION}": version,
        "{SPECIFIC_URL}": specificURL,
        "{SPECIFIC_SHA256}": specificHASH,
        "{GENERIC_URL}": genericURL,
        "{GENERIC_SHA256}": genericHASH,
    }

    flakeContent = template

    for key, value in toReplace.items():
        flakeContent = flakeContent.replace(key, value)
    
    return flakeContent

def generateFlake(version: str):
    urls = {
    "SPECIFIC": f"https://github.com/zen-browser/desktop/releases/download/{version}/zen.linux-specific.tar.bz2",
    "GENERIC": f"https://github.com/zen-browser/desktop/releases/download/{version}/zen.linux-generic.tar.bz2"
    }
    
    genericHASH, specificHASH = getSHA256s(genericURL=urls["GENERIC"], specificURL=urls["SPECIFIC"])
    flakeTemplate = getTemplate()
    flakeContent = generateFlakeContent(
        template=flakeTemplate, 
        version=version, 
        specificURL=urls["SPECIFIC"], 
        specificHASH=specificHASH, 
        genericURL=urls["GENERIC"], 
        genericHASH=genericHASH
    ) 
    
    # WRITE TO FLAXE.NIX
    flakePath = pathlib.Path("flake.nix")
    flakePath.touch()
    flakeFile = open(file=flakePath, mode="w")
    flakeFile.write(flakeContent)