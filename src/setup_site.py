import tomli
import os 
import json
from typing import List, Dict, Any

def getConfigFile(file_to_open: str):
    with open(file_to_open, "rb") as config_file:
        config = tomli.load(config_file)
    return config

def createTempFolder():
    return 0

def createOutputFolders():
    return 0

def getCSSFiles():
    return 0

def getJavascriptFiles():
    return 0

def createMainTemplate():
    return 0

def getListOfPosts(path_to_files: str) -> List[str]:
    list_of_posts: List[str] = []
    for files in os.listdir(path_to_files):
        if files.endswith(".md"):
            list_of_posts.append(os.path.join(path_to_files, files))
    return list_of_posts

def createPostsJSON(list_of_posts: List[str]):
    return 0