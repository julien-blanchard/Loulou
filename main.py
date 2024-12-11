# std libraries
import os
import shutil
from datetime import datetime
import json
from pprint import pprint
from collections import Counter
from typing import List, Dict, Any

# third party libraries
import mistune

# local modules 
from src.setup_site import *
from src.create_posts import *
from src.create_about import createAbout
from src.create_extras import createExtras

# Constants
CONFIG_FILE: str = "config.json"
NOW: str = datetime.now().strftime("%Y%m%d")
ROOT_DIR: str = os.getcwd()
OUTPUT_DIR: str = os.path.join(ROOT_DIR,"build")
DATA_DIR: str = os.path.join(ROOT_DIR,"data",NOW)
POSTS_DIR: str = os.path.join(ROOT_DIR,"posts")
TEMPLATES_DIR: str = os.path.join(ROOT_DIR,"templates")
OUTPUT_FOLDERS: List[str] = [
    "css",
    "images",
    "javascript",
    "pages",
    "posts"
]

# Often re-used
config_file: Dict = getConfigFile(CONFIG_FILE)
template_main: str = os.path.join(DATA_DIR,"custom_main.html")

def setupSite() -> None:
    createDataFolder(DATA_DIR)
    clearOutputFolder(OUTPUT_DIR)
    createOutputFolders(OUTPUT_DIR,OUTPUT_FOLDERS)
    createMainTemplate(ROOT_DIR,DATA_DIR,f'{config_file["main"]["author"]} {NOW[:4]}')
    moveToOutputFolders(ROOT_DIR,OUTPUT_DIR,"css")
    moveToOutputFolders(ROOT_DIR,OUTPUT_DIR,"javascript")

def createPosts() -> None:
    list_of_posts: List[str] = getListOfPosts(POSTS_DIR)
    createPostsJSON(list_of_posts,DATA_DIR)

def createNavigation() -> None:
    createAbout(DATA_DIR,TEMPLATES_DIR,OUTPUT_DIR)
    createExtras(DATA_DIR,TEMPLATES_DIR,OUTPUT_DIR)

if __name__ == "__main__":
    setupSite()
    createPosts()
    createNavigation()