import json 
import os
from typing import List, Dict, Any
import mistune
    
def createPost(post_path: str, templates: List[str], output_dir: str, attributes: List[str]):
    with open(post_path,"r") as temp_file:
        temp_post: str = temp_file.read()
    
    post_no_header: str = temp_post.split("-----")[2]
    post_body: str = (
        mistune
        .html(post_no_header)
        .replace('<a href=','<a class="has-text-danger" href=')
        .replace('<img src="','<img class="images-centre" src="https://blanchardjulien.com')
        .replace("<yt>",'<iframe width="90%" height="430" src="https://www.youtube.com/embed/')
        .replace("</yt>",'" frameborder="0" allowfullscreen></iframe>')
    )

    full_post: str = (
        templates[0]
        .replace('<script>','<script>\n\t\thljs.highlightAll();\n')
        .replace("{{placeholder_content}}",templates[1])
        .replace("{{placeholder_post_title}}",attributes[0])
        .replace("{{placeholder_post_date}}",attributes[1])
        .replace("{{placeholder_post_tags}}",attributes[2])
        .replace("{{placeholder_post_readtime}}",attributes[3])
        .replace("{{placeholder_post_content}}",post_body)
    )
    post_name: str = f'{os.path.split(post_path)[-1].split(".")[0]}.html'
    path_to_post: str = os.path.join(output_dir,"posts",post_name)
    with open(path_to_post,"w") as temp_file:
        temp_file.write(full_post)

def createIndividualPosts(json_path: str, html_template: str,template_folder: str, posts_folder: str, output_dir: str) -> None:
    with open(os.path.join(html_template,"custom_main.html"), "r") as template_file:
        main_html: str = template_file.read()
    with open(os.path.join(template_folder,"template_individual_post.html"), "r") as template_file:
        individual_post_html: str = template_file.read()
    html_templates: List[str] = [main_html,individual_post_html]

    with open(json_path,"r") as file_json:
        json_as_string: str = file_json.read()
        json_posts = json.loads(json_as_string)

    for posts in json_posts:
        post_title: str = json_posts[posts]["title"].title()
        post_date: str = json_posts[posts]["date"]
        post_tags: str = ", ".join(json_posts[posts]["tags"])
        post_readtime: str = json_posts[posts]["readTime"]
        post_attributes: List[str] = [
            post_title,
            post_date,
            post_tags,
            post_readtime
        ]
        path_to_post: str = os.path.join(posts_folder,posts)
        createPost(path_to_post,html_templates,output_dir,post_attributes)