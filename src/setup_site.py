import os 
import shutil
import json
from typing import List, Dict, Any

def getConfigFile(file_to_open: str) -> Dict:
    with open(file_to_open, "rb") as config_file:
        config = json.load(config_file)
    return config

def createDataFolder(path_to_folder: str) -> None:
    if not os.path.exists(path_to_folder):
        os.mkdir(path_to_folder)

def clearOutputFolder(path_to_folder: str) -> None:
    for folder_or_file in os.listdir(path_to_folder):
        path = os.path.join(path_to_folder, folder_or_file)
        if os.path.isfile(path):
            os.remove(path)
        else:
            clearOutputFolder(path)
    os.rmdir(path_to_folder)

def createOutputFolders(path_to_folder: str, subfolder_names: List[str]) -> None:
    if not os.path.exists(path_to_folder):
        os.mkdir(path_to_folder)
    for subfolders in subfolder_names:
        subfolder = os.path.join(path_to_folder,subfolders)
        if not os.path.exists(subfolder):
            os.mkdir(subfolder)

def createMainTemplate(path_to_input_file: str, path_to_output_file: str, footer) -> str:
    template_file_location: str = os.path.join(path_to_input_file,"templates","template_main.html")
    with open(template_file_location,"r") as template_file:
        template_string: str = template_file.read()
        template_string = (
            template_string
            .replace("{{placeholder_footer}}",footer)
            )
    with open(os.path.join(path_to_output_file,"custom_main.html"),"w") as custom_file:
        custom_file.write(template_string)
    return template_string

def moveToOutputFolders(copy_folder: str, paste_folder: str, file_type: str) -> None:
    for files_to_copy in os.listdir(os.path.join(copy_folder,file_type)):
        copy: str = os.path.join(copy_folder,file_type,files_to_copy)
        paste: str = os.path.join(paste_folder,file_type,files_to_copy)
        shutil.copy(copy,paste)

def getCSSFiles(css_files: List[str], path_to_folder: str) -> List[str]:
    result: List[str] = []
    for css in css_files:
        target: str = f"{path_to_folder}/css/{css}"
        html_code: str = f'<link rel="stylesheet" href="{target}">'
        result.append(html_code)
    return result

def getJavascriptFiles(js_files: List[str], path_to_folder: str) -> List[str]:
    result: List[str] = []
    for js in js_files:
        target: str = f"{path_to_folder}/javascript/{js}"
        html_code: str = f'<script src="{target}"></script>'
        result.append(html_code)
    return result