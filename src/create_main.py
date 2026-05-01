import os
from datetime import datetime

def createMainTemplate(path_to_input_file: str, path_to_output_file: str, config_file) -> str:
    template_file_location: str = os.path.join(path_to_input_file,"templates","template_main.html")
    with open(template_file_location,"r") as template_file:
        template_string: str = template_file.read()
    template_string = (
        template_string
       .replace("{{placeholder_url}}",config_file["main"]["url"])
       .replace("{{placeholder_title}}",config_file["main"]["title"])
       .replace("{{placeholder_subtitle}}",config_file["main"]["subtitle"])
       .replace("{{placeholder_author}}",config_file["main"]["author"])
       .replace("{{placeholder_picture}}",config_file["main"]["profilePicture"])
       .replace("{{placeholder_footer}}",f'{config_file["main"]["author"]} {datetime.now().strftime("%Y")}')
       .replace("{{placeholder_github}}",config_file["social"]["gitHub"])
       .replace("{{placeholder_linkedin}}",config_file["social"]["linkedIn"])
    )

    css_includes = [
        f'\t<link rel="stylesheet" href="{config_file["main"]["url"]}/css/{css_file}">'
        for css_file in config_file["css"]
    ]
    css_section = "\n".join(css_includes)
    template_string = (
        template_string
       .replace("{{placeholder_css}}",css_section)
    )

    js_includes = []
    for js_file in config_file["js"]:
        options = [
            f' {option}' if value is True else f' {option}="{value}"'
            for option, value in js_file["options"].items()
        ]
        options_string = "".join(options) 
        js_includes.append(f'\t<script src="{js_file["url"]}"{options_string}></script>')

    js_section = "\n".join(js_includes)
    template_string = (
        template_string
       .replace("{{placeholder_js}}",js_section)
    )

    with open(os.path.join(path_to_output_file,"custom_main.html"),"w") as custom_file:
        custom_file.write(template_string)
    return template_string


def createJavaScript(js_file_location: str, target_folder: str, config_file) -> str:
    with open(js_file_location,"r") as js_file:
        template_string: str = js_file.read()
    template_string = (
        template_string
       .replace("{{placeholder_github}}",config_file["social"]["gitHub"])
       .replace("{{placeholder_linkedin}}",config_file["social"]["linkedIn"])
    )
    with open(os.path.join(target_folder, "javascript", "script.js"),"w") as custom_file:
        custom_file.write(template_string)

