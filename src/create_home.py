import json 
import os
from typing import List, Dict, Any
import mistune

def createLatestArticles(json_file, num_of_articles: int) -> str:
    html_list = '<li><span class="tag">{}</span> &emsp; <a class="has-text-danger" href="{}">{}</a></li>'
    target_url = "https://blanchardjulien.com/posts/"
    result = result.replace("{{placeholder_posts}}","")
    return result

def getFeaturedArticles() -> str:
    return ""

x = """
<div class="cell">
  <div class="card">
    <header class="card-header">
      <p class="card-header-title">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit
      </p>
    </header>
    <div class="card-content">
      <div class="content">
        Ut enim ad minim veniam
      </div>
    </div>
    <footer class="card-footer">
      <a href="#" class="card-footer-item has-text-danger">Read more</a>
    </footer>
  </div>
</div>
"""





