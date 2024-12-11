import json 
import os
from typing import List, Dict, Any
import mistune

def getListOfPosts(path_to_files: str) -> List[str]:
    result: List[str] = []
    for files in os.listdir(path_to_files):
        if files.endswith(".md"):
            result.append(os.path.join(path_to_files, files))
    result.reverse()
    return result

def createPostsJSON(list_of_posts: List[str], path_to_json: str):
    temp_container = []
    for posts in list_of_posts:
        with open(posts, "r") as post_file:
            post: str = post_file.read()
            post_config = post.split("---")[1]
            post_content: str = post.split("---")[-1]
            post_title: str = posts.split("\\")[-1] # windows
            # post_title: str = posts.split("/")[-1] # linux
            post: str = f'"{post_title}": {post_config}'
            temp_container.append(post)
    temp_container = ",".join(temp_container)
    temp_container = "{" + temp_container + "}"
    result = json.loads(temp_container)

    json_file_name: str = os.path.join(path_to_json,"posts.json")
    with open(json_file_name,"w") as json_file:
        json.dump(result,json_file)
        
    return result

def markdownToHtml(data: str) -> str:
    html: str = mistune.html(data)
    result: str = (
        html
        .replace("","")
        .replace("","")
        .replace("","")
    )
    return html
    # return result

