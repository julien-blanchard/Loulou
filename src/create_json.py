import json 
import os
from typing import List, Dict, Any
from collections import OrderedDict

def getListOfPosts(path_to_files: str) -> List[str]:
    result: List[str] = []
    for files in os.listdir(path_to_files):
        if files.endswith(".md"):
            result.append(os.path.join(path_to_files, files))
    result.reverse()
    return result

def createPostsJSON(list_of_posts: List[str], path_to_json: str) -> Dict:
    temp_container: List[str] = []
    for posts in list_of_posts:
        with open(posts, "r", encoding="utf8") as post_file:
            post: str = post_file.read()
            post_config = post.split("-----")[1]
            post_content: str = post.split("-----")[-1]
            post_title: str = os.path.split(posts)[-1]
            post: str = f'"{post_title}": {post_config}'
            temp_container.append(post)
    temp_container = ",".join(temp_container)
    temp_container = "{" + temp_container + "}"
    unsorted_result = json.loads(temp_container)
    result = OrderedDict(reversed(sorted(unsorted_result.items())))

    json_file_name: str = os.path.join(path_to_json,"posts.json")
    with open(json_file_name,"w", encoding="utf8") as json_file:
        json.dump(result,json_file)
        
    return result

