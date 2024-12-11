---
title: "Building a simple documentation tool with Mistune and Pico.css"
date: 2024-08-18
summary: "Whether at work or in my personal time, one thing I particularly enjoy is to try and come up with my own set of tools"
draft: false
---

<script src="https://cdn.counter.dev/script.js" data-id="205ad799-38b0-4d9a-ac65-2fdf615ff871" data-utcoffset="0"></script>

*An example of what we’ll be discussing in this article*

![alt text](/images/md_to_html03.png "Image")

Whether at work or in my personal time, one thing I particularly enjoy is to try and come up with my own set of tools. Now don't get me wrong, I wouldn't have the skills to build and maintain anything even somewhat complicated. So just to be clear, we're not talking here about writing a compiler or anything that even approaches that level of complexity.

My actual goal is fairly simple: whenever I can, I write my own code rather than rely on third-party libraries and frameworks. Generally speaking, I genuinely think that this is a good exercise and if you're reading this article I hope that you too enjoy witing your own linear regressions, text parsers, and so forth.. If you're a beginner [**Python**](https://www.python.org/) user, a good place to start is to for instance avoid using the [**collections**](https://docs.python.org/3/library/collections.html) module and its `Counter()` *subclass* if you want to count the *n* number of elements within a list.

And so over the years I have built a decent amount of small utility tools. If I am to be honest though I will have to admit that I have ended up abandoning pretty much all of them.

There is however this one specific script that I still use on an almost weekly basis: a simple program that allows me to create some fancy-looking and easy-to-use documentation for the projects I'm involved in.

At a high-level, what this script does is convert a text in *markdown* format into an *html* page. Allow me to try and convince you:

*  It's easy to deploy and use on a day-to-day basis
*  It looks and feels much better than your average **Word** document
*  You can easily bookmark an *html* file in your favourite browser, making it super simple to centralise all your documentation
*  Everybody knows **Markdown**
*  The folks you work with will be able to read your document, but not to edit them (unless they edit the corresponding **Markdown** file and run the **Python** script that we're about to write)

This sounds promising, so let's get started!

# Mistune VS Markdown

Every **Python** programmer that has one day looked for a library that can easily convert *markdown* to *html* has most likely found themselves facing the following choice: should I use the standard [**Markdown**](https://python-markdown.github.io/) library, or go for a popular but third-party package called [**Mistune**](https://mistune.lepture.com/en/latest/)?

Let me cut to the chase: we'll be going with the second option. And the reason behind this is quite simple: I have personally had a much better experience using **Mistune**, while **Markdown** seems more prone to messing up with code blocks and *html* tags.

Converting your first *markdown* text to *html* couldn't be simpler:

```python
import mistune

md: str = """
# This is a title

This text is <kbd>highlighted</kbd>

*  This is a list
"""

html: str = mistune.html(md)
print(html)
``` 

![alt text](/images/md_to_html01.png "Image")

As you might have noticed, we had sneakily inserted an *html* tag inside our *markdown* text, and **Mistune** left it as is. Let's keep this in mind, as it's going to prove extremely valuable at a later stage when we want to work with some specific *html* elements. But before we get there, what we should do next is create an *html* file named `template.html` and paste into it the following boilerplate code:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{{document_title}}</title>
    <link rel="stylesheet" href={{css_framework}}>
  </head>
  <body>
	{{markdown_file}}
  </body>
</html>
```

See these weird `{{document_title}}`, `{{css_framework}}` and `{{markdown_file}}` placeholder *strings*? As you've probably already guessed, we'll be replacing these temporary fields with actual chunks of code in a little while. We've a good bit of work to do before we get there though!

On a related note, you might be wondering if we could tell our default browser to open that new `document.html` file that we just created. Luckily for us, **Python** has this great library named [**Webbrowser**](https://docs.python.org/3/library/webbrowser.html) that we can use to automatically open any *html* file.

# Structure

Right, now that we have a rough idea of how we can generate a simple *html* webpage, it's high time we started thinking about how we want to structure our document template.

We should probably start by defining some guiding principles. Our final product should:

*  Keep things simple
*  Have a clean UI
*  Be easy to navigate

With these constraints in mind, the best possible layout is I think the following one:

1.  A title
2.  Some very high-level information: the owner / creator of the document, and the last update date
3.  One or multiple collapsable sections for each main block of text

Now that should be pretty straightforward. For instance, each collapsable section will ultimately more or less resemble the following lines of *html* code:

```html
<details><summary role="button">The title of our section goes here</summary>

Some content here

</details>
```

Now one issue here is that we clearly stated in our guiding principles that we wanted to keep things as simple as possible. To be honest, having to write all this boilerplate *html* code kind of goes against the main goal of what we're trying to achieve here. But guess what, we can easily solve that issue!

# Customising our markdown parser

Markdown has some reserved signs, such as wrapping some text around double star characters `**bold**`

We're going to need to add our own customised commands though. Here are the ones I use:

1.  The first line of our *markdown* file will always have to contain the following structure:

`[title],[owner 1],[owner 2 (optional)],[owner 3 (optional)],etc..`

Like this:

```markdown
This is a document,Julien,Fiona
```

2.  Each section should always be wrapped around the  following structure:

`BEGIN,[section title]` and `END`

As in:

```markdown
BEGIN,Pizza

Pizzas are **awesome**

END
```

In other words, the simplest expression of our *md* file should look like this:

```markdown
This is a document,Julien,Fiona

Hi, I like junk food!

BEGIN,Pizza

Pizzas are **awesome**

END
```

Right now, if we were to parse this arguably more simpler version of the *html* tags we wrote in the previous section, nothing special would happen. What we have to do is write a couple of functions that can help us use this augmented syntax and transform it into our target *html* code.

First things first, let's import some libraries and create a `class` *object* that we're going to name `MarkdownParser` (I know, I've never been a creative guy):

```python
import mistune
import sys 
import os
from datetime import datetime
from typing import List, Set, Dict, Tuple

class MarkdownParser: 

    def __init__(self):
        self.file_name: str = sys.argv[1]
        self.last_updated: str = datetime.now().strftime("%Y-%m-%d")
        self.first_line: str = ""
        self.title: str = ""
        self.html_boilerplate: str = """
            <!DOCTYPE html>
            <html lang="en" data-theme="dark">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>{{document_title}}</title>
                <link rel="stylesheet" href={{css_framework}}>
            </head>
            <body>
                <div class="container">
                    {{markdown_file}}
                </div>
            </body>
            </html>
        """
```

Our `__init__` function will contain the *html* boilerplate that we used earlier on, as well as the following variables:

*  We'll be using `self.file_name` to grab the local *md* file that contains our documentation in **markdown** format
*  `self.last_updated` refers to the day on which we last ran our **Python** script for a given document
*  `self.first_line` is an empty string at the moment, but will be used at a later stage to store the first line of our document
*  Finally, we'll replace the `{{document_title}}` placeholder that's currently sitting within our *html* boilerplate with the value stored in `self.title`

Still within our `MarkdownParser` class, let's create a new function to load the *md* file that we want to parse:

```python
def fetchMarkdown(self) -> str:
    with open(self.file_name, "r") as file:
        fetched_md: str = file.readlines()
    self.first_line = fetched_md[0]
    return fetched_md
```

Please note that we're storing each line of our document within a *list* using the `readlines()` method.

We're also sending the first of these lines to the `self.first_line` variable that we created when initialising our `MarkdownParser` *object*. If you remember, this first line should always be in the following format: `[title],[owner 1],[owner 2 (optional)],[owner 3 (optional)],etc..`

Our next function, `getHeader()`, will transform that first line into a the desired *html* format:

```python
def getHeader(self) -> str:
    first_line_as_list: List[str] = self.first_line.split(",")
    self.title: str = first_line_as_list[0]
    parsed_header: str = ""
    parsed_header += f'<div class="header"><h1>{first_line_as_list[0]}</h1></div>'
    if len(first_line_as_list) > 2:
        parsed_header += "<p>Owners:</p>"
    else:
        parsed_header += "<p>Owner:</p>"
    parsed_header += "<ul>" 
    for line in first_line_as_list[1:]:
        parsed_header += f'<li>{line}</li>'
    parsed_header += "</ul>"
    parsed_header += f"<p>Last updated: <kbd>{self.last_updated}</kbd></p>" 
    parsed_header += "<br>"
    return parsed_header
```

What we did here is pretty straightforward:

1.  After splitting the first line of our *md* file into a *list* named `first_line_as_list`, we sent the first element of this *list* to the `self.title` variable that we had created a couple of minutes ago. This will now be the title of our *html* webpage when we open it in our browser
2.  The very same value is then re-used to become the title of our document
3.  We then assess whether or not there is one or multiple owners for this document, and convert the remaining element(s) of `first_line_as_list` into an *html* list
4.  Last but not least, we fetch the `self.last_updated` *string* that was automatically created when we initialised the `MarkdownParser` *object* and nest is between a pair of `<kbd></kbd>` tags

Using a similar approach, our next step is to create a function that parses the rest of the *md* file:

```python
def getBody(self,fetched_md) -> str:
    parsed_body: str = ""
    for line in fetched_md[1:]:
        if line.startswith("BEGIN"):
            section_title: str = line.split(",")[1]
            new_section: str = f'<details><summary role="button">{section_title}</summary>'
            parsed_body += new_section
        elif line.startswith("END"):
            parsed_body += "</details>"
        else:
            parsed_body += f" {line} "
    return parsed_body 
```

Alright, now that we have some basic parsing functions we can combine their output and use **Mistune** to convert that whole piece of *markdown* text into its corresponding *html* blocks:

```python
def convertToHTML(self) -> str:
    md_as_list: str = self.fetchMarkdown()
    document_header: str = self.getHeader()
    document_body: str = self.getBody(md_as_list)
    full_document: str = document_header + document_body
    md_to_html: str = mistune.html(
        full_document
    )
    html_final: str = (
        self.html_boilerplate
        .replace(
            "{{document_title}}",
            self.title
        )
        .replace(
            "{{markdown_file}}",
            md_to_html
        )
        .replace(
            "<code>",
            "<pre><code>"
        )
        .replace(
            "</code>",
            "</pre></code>"
        )
    )
    return html_final
```

We're getting there! As you can see, we have chained some `.replace()` methods to fill in the placeholder values that we had defined earlier in this article. We also made some slight changes to the *html* code blocks, but that part is purely optional.

Next, we of course need to save the output of our `convertToHTML()` function into a proper *html* file:

```python
def saveFile(self):
    html_final: str = self.convertToHTML()
    html_file_name: str = f"{self.file_name.split('.')[-2]}.html"
    with open(html_file_name,"w") as file:
        file.write(html_final)
```

We're finally done with our `MarkdownParser` *class*, so let's give it a try and make sure everything works as intended:

```python
if __name__ == "__main__":
    mp = MarkdownParser()
    try:
        mp.saveFile()
    except Exception as e:
        print(e)
```

![alt text](/images/md_to_html02.png "Image")

# CSS themes

The good news is, our parser does what it's expected to do. But the result still looks awful, right?

At this point, what we could do is write some *css* code, or use a framework like [**Tailwind**](https://tailwindcss.com/), [**Bulma**](https://bulma.io/) or even [**Bootstrap**](https://getbootstrap.com/). But as we want to keep things as simple as possible, we're instead going to use a *minimalist css framework*. Now if you're not familiar with what a *minimal css framework* is, I suggest heading over to [this article](https://blanchardjulien.com/posts/minimalist_css/) that I wrote about a year or so ago. The ones that I think suit our little *markdown* parser best are:

*  [**Pico.css**](https://picocss.com/)
*  [**LaTex.css**](https://latex.vercel.app/)
*  [**Simple.css**](https://simplecss.org/)

If you remember when we initialised our `MarkdownParser` *class*, we created a variable named `self.html_boilerplate` and left a placeholder there for some *css* file or url that we said we'd take care of later:

```html
<link rel="stylesheet" href={{css_framework}}>
```

Still within this `__init__()` function, let's add three new variables:

```python
self.pico: str = "https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css"
self.latex: str = "https://latex.now.sh/style.css"
self.simple: str = "https://cdn.simplecss.org/simple.min.css"
```

Now let's head back to the `convertToHTML()` function that we created a few minutes ago, and append the following `.replace()` method to the `self.html_boilerplate` *string* variable:

```python
html_final: str = (
    self.html_boilerplate

...

    .replace(
        "{{css_framework}}",
        self.pico
    )
)
```

![alt text](/images/md_to_html03.png "Image")

After we re-run the whole script we are greeted with this arguably much better-looking *html* page.

# Final thoughts

As discussed in the opening lines of this article, I really like the simplicity and usefulness of this little text parsing tool. 

Over the years this script has allowed me to write and share some supporting documentation for pretty much all the small to large projects I've been involved in. All I need to do is open up my terminal and run `python3 [name_of_your_markdown_parser_file].py [name_of_your_markdown_file].md`. It's literally as simple as that.

Feel free to re-use and modify the code we wrote together, and don't hesitate to reach out to me if you've any feedback or suggestions!

# Full code:

```python
import mistune
import sys 
import os
from datetime import datetime
from typing import List, Set, Dict, Tuple

class MarkdownParser: 

    def __init__(self):
        self.pico: str = "https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css"
        self.latex: str = "https://latex.now.sh/style.css"
        self.simple: str = "https://cdn.simplecss.org/simple.min.css"
        self.file_name: str = sys.argv[1]
        self.last_updated: str = datetime.now().strftime("%Y-%m-%d")
        self.first_line: str = ""
        self.title: str = ""
        self.html_boilerplate: str = """
            <!DOCTYPE html>
            <html lang="en" data-theme="dark">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>{{document_title}}</title>
                <link rel="stylesheet" href={{css_framework}}>
            </head>
            <body>
                <div class="container">
                    {{markdown_file}}
                </div>
            </body>
            </html>
        """

    def fetchMarkdown(self) -> str:
        with open(self.file_name, "r") as file:
            fetched_md: str = file.readlines()
        self.first_line = fetched_md[0]
        return fetched_md
    
    def getHeader(self) -> str:
        first_line_as_list: List[str] = self.first_line.split(",")
        self.title: str = first_line_as_list[0]
        parsed_header: str = ""
        parsed_header += f'<div class="header"><h1>{first_line_as_list[0]}</h1></div>'
        if len(first_line_as_list) > 2:
            parsed_header += "<p>Owners:</p>"
        else:
            parsed_header += "<p>Owner:</p>"
        parsed_header += "<ul>" 
        for line in first_line_as_list[1:]:
            parsed_header += f'<li>{line}</li>'
        parsed_header += "</ul>"
        parsed_header += f"<p>Last updated: <kbd>{self.last_updated}</kbd></p>" 
        parsed_header += "<br>"
        return parsed_header
    
    def getBody(self,fetched_md) -> str:
        parsed_body: str = ""
        for line in fetched_md[1:]:
            if line.startswith("BEGIN"):
                section_title: str = line.split(",")[1]
                new_section: str = f'\n<details><summary role="button">{section_title}</summary>\n'
                parsed_body += new_section
            elif line.startswith("END"):
                parsed_body += "\n</details>\n"
            else:
                parsed_body += f"\n {line} \n"
        return parsed_body 
    
    def convertToHTML(self) -> str:
        md_as_list: str = self.fetchMarkdown()
        document_header: str = self.getHeader()
        document_body: str = self.getBody(md_as_list)
        full_document: str = document_header + document_body
        md_to_html: str = mistune.html(
            full_document
        )
        html_final: str = (
            self.html_boilerplate
            .replace(
                "{{document_title}}",
                self.title
            )
            .replace(
                "{{markdown_file}}",
                md_to_html
            )
            .replace(
                "<code>",
                "<pre><code>"
            )
            .replace(
                "</code>",
                "</pre></code>"
            )
            .replace(
                "{{css_framework}}",
                self.pico
            )
        )
        return html_final
    
    def saveFile(self):
        html_final: str = self.convertToHTML()
        html_file_name: str = f"{self.file_name.split('.')[-2]}.html"
        with open(html_file_name,"w") as file:
            file.write(html_final)

if __name__ == "__main__":
    mp = MarkdownParser()
    try:
        mp.saveFile()
    except Exception as e:
        print(e)
```
