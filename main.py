# libraries
import os
from datetime import datetime
import mistune
import tomli
from collections import Counter
from typing import List, Dict, Any

# Constants
CONFIG_FILE: str = "config.toml"
NOW: str = datetime.now().strftime("%Y-%m-%d")
ROOT_DIR: str = os.getcwd()
OUTPUT_DIR: str = os.path.join(ROOT_DIR,"build")
OUTPUT_FOLDERS: List[str] = [
    "css",
    "images",
    "javascript",
    "pages",
    "posts"
]

# Functions

def setupSite():
    return 0

def createHome():
    return 0

def createPosts():
    return 0

def createPostsList():
    return 0

def createAbout():
    return 0

def runAll() -> None:
    try:
        setupSite()
        createHome()
        createPosts()
        createPostsList()
        createAbout()
    except Exception as e:
        print(e)

# Functions
if __name__ == "__main__":
    runAll()
