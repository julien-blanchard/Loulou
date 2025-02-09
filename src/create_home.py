import json 
import os
from typing import List, Dict, Any

def createLatestArticles(json_file: Dict, num_of_articles: int, url: str) -> str:
    temp_container: List[str] = []
    for posts in json_file: 
      post_title: str = json_file[posts]["title"].title()
      post_path: str = f"{url}/posts/{posts.split(".")[0]}.html"
      post_date: str = json_file[posts]["date"]
      html_list: str = f'<li><span class="tag">{post_date}</span> &emsp;<a class="has-text-danger" href="{post_path}">{post_title}</a></li>'
      temp_container.append(html_list)
    result: str = "\n".join(temp_container[:num_of_articles])
    return result

def getFeaturedArticles(json_file: Dict, url: str) -> str:
    temp_container: List[str] = []
    for posts in json_file:
      if json_file[posts]["featured"] is True:
        post_title: str = json_file[posts]["title"].title()
        post_path: str = f"{url}/posts/{posts.split(".")[0]}.html"
        post_summary: str = json_file[posts]["summary"]
        html_cell: str = f"""
        <div class="cell">
          <div class="card">
            <header class="card-header">
              <p class="card-header-title">
                {post_title}
              </p>
            </header>
            <div class="card-content">
              <div class="content">
                {post_summary}
              </div>
            </div>
            <footer class="card-footer">
              <a href="{post_path}" class="card-footer-item has-text-danger">Read more</a>
            </footer>
          </div>
        </div>
        """
        temp_container.append(html_cell)
    result: str = "\n".join(temp_container)
    return result

def createIndex(html_template: str,template_folder: str,target_folder: str,latest,featured) -> None:
    with open(os.path.join(html_template,"custom_main.html"), "r") as template_file:
        main_html: str = template_file.read()
    with open(os.path.join(template_folder,"template_home.html"), "r") as template_file:
        home_html: str = template_file.read()

    home_html: str = (
        home_html
        .replace("{{placeholder_latest_articles}}",latest)
        .replace("{{placeholder_featured_articles}}",featured)
    )
    result = main_html.replace(
        "{{placeholder_content}}",home_html
    )

    with open(os.path.join(target_folder,"index.html"), "w") as template_file:
        template_file.write(result)

def createHome(json_path: str, num_of_articles: int, url: str, html_template: str,template_folder: str,target_folder: str) -> None:
    with open(json_path,"r") as file_json:
        json_as_string: str = file_json.read()
        json_posts: Dict = json.loads(json_as_string)

    latest_articles: str = createLatestArticles(json_posts,num_of_articles,url)
    featured_articles: str = getFeaturedArticles(json_posts,url)
    createIndex(html_template,template_folder,target_folder,latest_articles,featured_articles)







