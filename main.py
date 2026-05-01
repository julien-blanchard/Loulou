# std libraries
import os
import shutil
from datetime import datetime
import json
from pprint import pprint
from collections import Counter, OrderedDict
from typing import List, Dict, Any

# third party libraries
import mistune

# local modules 
from src.setup_site import *
from src.create_json import *
from src.create_main import createMainTemplate, createJavaScript
from src.create_about import createAbout
from src.create_extras import createExtras
from src.create_home import createHome
from src.create_postspage import createPostsPage
from src.create_individualposts import createIndividualPosts

# Constants
CONFIG_FILE: str = "config.json"
JS_FILE: str = "javascript/script.js"
ROOT_DIR: str = os.getcwd()
OUTPUT_DIR: str = os.path.join(ROOT_DIR,"build")
DATA_DIR: str = os.path.join(ROOT_DIR,"data")
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
json_file: str = os.path.join(DATA_DIR,"posts.json")

# Wrapper functions
def setupSite() -> None:
    createFolders(
        OUTPUT_DIR,
        DATA_DIR
    )
    clearOutputFolder(OUTPUT_DIR)
    createOutputFolders(
        OUTPUT_DIR,
        OUTPUT_FOLDERS
    )
    moveToOutputFolders(
        ROOT_DIR,
        OUTPUT_DIR,
        "css"
    )
    moveToOutputFolders(
        ROOT_DIR,
        OUTPUT_DIR,
        "javascript"
    )
    moveToOutputFolders(
        ROOT_DIR,
        OUTPUT_DIR,
        "images"
    )

def createJSON() -> None:
    list_of_posts: List[str] = getListOfPosts(POSTS_DIR)
    createPostsJSON(
        list_of_posts,
        DATA_DIR
    )

def createPages() -> None:
    createJavaScript(
        JS_FILE,
        OUTPUT_DIR,
        config_file
    )
    createMainTemplate(
        ROOT_DIR,
        DATA_DIR,
        config_file
    )
    createAbout(
        DATA_DIR,
        TEMPLATES_DIR,
        OUTPUT_DIR
    )
    createExtras(
        DATA_DIR,
        TEMPLATES_DIR,
        OUTPUT_DIR
    )
    createHome(
        json_file,
        7,
        config_file["main"]["url"],
        DATA_DIR,
        TEMPLATES_DIR,
        OUTPUT_DIR
    )
    createPostsPage(
        json_file,
        7,
        config_file["main"]["url"],
        DATA_DIR,
        TEMPLATES_DIR,
        OUTPUT_DIR
    )

def createContent() -> None:
    createIndividualPosts(
        json_file,
        DATA_DIR,
        TEMPLATES_DIR,
        POSTS_DIR,
        OUTPUT_DIR,
        config_file
    )

if __name__ == "__main__":
    setupSite()
    createJSON()
    createPages()

    createContent()

