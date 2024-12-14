import json 
import os
from typing import List, Dict, Any
from collections import Counter

def createTopTags(json_file: Dict, num_of_tags: int, url: str) -> str:
    temp_container: List[str] = []
    tags: List[List[str]] = [json_file[posts]["tags"] for posts in json_file]
    cleanded_tags: List[str] = [tag for nested_tags in tags for tag in nested_tags]
    for c in Counter(cleanded_tags).most_common(num_of_tags):
        html_list: str = f'<tag class="button is-danger">{c[0]} {c[1]}</tag>'
        temp_container.append(html_list)
    result: str = "\n".join(temp_container)
    return result

def createPostsList(json_file: Dict, url: str) -> str:
    temp_container: Dict = {}
    for posts in json_file:
        idx: str = posts[:4]
        post_date: str = json_file[posts]["date"]
        post_path: str = f'{url}/posts/{posts.split(".")[0]}.html'
        post_title: str = json_file[posts]["title"].title()
        post_data: List[str] = [post_date,post_path,post_title]
        if idx in temp_container:
            temp_container[idx].append(post_data)
        else:
            temp_container[idx] = [post_data]

    result: List[str] = []    
    for year, post_row in temp_container.items():
        html_year_top: str = f'''
        <h3 class="has-text-left has-text-centered-mobile">{year}</h3>
            <div class="block has-text-left">
                <ul>
        '''
        html_year_bottom: str = f'''
            </ul>
        </div>
        '''
        result.append(html_year_top)
        for post in post_row:
            html_list: str = f'<li><span class="tag">{post[0]}</span> &emsp; <a class="has-text-danger" href="{post[1]}">{post[2]}</a></li>'
            result.append(html_list)
        
        result.append(html_year_bottom)
    result = "\n".join(result)
    return result

def createPostsIndex(html_template: str,template_folder: str,target_folder: str,tags: str,posts: str) -> None:
    with open(os.path.join(html_template,"custom_main.html"), "r") as template_file:
        main_html: str = template_file.read()
    with open(os.path.join(template_folder,"template_page_posts.html"), "r") as template_file:
        posts_list_html: str = template_file.read()

    posts_list_html: str = (
        posts_list_html
        .replace("{{placeholder_top_tags}}",tags)
        .replace("{{placeholder_all_posts}}",posts)
    )
    result = main_html.replace(
        "{{placeholder_content}}",posts_list_html
    )

    with open(os.path.join(target_folder,"pages","posts.html"), "w", encoding="utf8") as template_file:
        template_file.write(result)

def createPostsPage(json_path: str, num_of_tags: int, url: str, html_template: str,template_folder: str,target_folder: str) -> None:
    with open(json_path,"r",encoding="utf8") as file_json:
        json_as_string: str = file_json.read()
        json_posts = json.loads(json_as_string)
    
    top_tags: str = createTopTags(json_posts, num_of_tags, url)
    posts_list: str = createPostsList(json_posts, url)
    createPostsIndex(html_template,template_folder,target_folder,top_tags,posts_list)