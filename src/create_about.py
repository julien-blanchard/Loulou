import os

def createAbout(html_template: str, template_folder: str, target_folder: str) -> None:
    with open(os.path.join(html_template,"custom_main.html"), "r") as template_file:
        main_html: str = template_file.read()
    with open(os.path.join(template_folder,"template_about.html"), "r") as template_file:
        about_html: str = template_file.read()
    result: str = main_html.replace("{{placeholder_content}}",about_html)

    with open(os.path.join(target_folder,"pages","about.html"), "w") as template_file:
        template_file.write(result)
    