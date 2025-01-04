![Project status](https://img.shields.io/badge/version-1.0-green)
![Python version](https://img.shields.io/badge/requires-python_3.6-blue)

# :love_letter: **Loulou** :love_letter:

Loulou is a simple static site generator written in **Python**. It was primarily designed to build my personal website, [blanchardjulien.com](https://blanchardjulien.com/). But you are more than welcome to use it to create your own website.

# How does Loulou work?

Loulou relies on the following *css* and *javascript* libraries:

*  [Bulma](https://bulma.io/)
*  [Bulmaswatch](https://jenil.github.io/bulmaswatch/)
*  [Fontawesome](https://fontawesome.com/)
*  [Highlight.js](https://highlightjs.org/)
*  [Google's Space Mono font](https://fonts.google.com/)

# How to run Loulou?

You'll need to have the *python* language installed on your device, as well as the [mistune](https://mistune.lepture.com/en/latest/) library.

Once this done, simply:

1.  Modify the `template_main.html` file that you'll find in the `templates` directory
2.  Add the following header to your *markdown* articles and place them into the `posts` directory:

```
-----
{
"title":"",
"date":"",
"summary":"",
"tags":["",""],
"featured":false,
"readTime":""
}
-----

Start writing your article here!
```

3.  Name your *markdown* articles as follows: `YYMMDD_name_of_the_article.md`

Before you run the `main.py` file, you'll need two new directories at the root of your project:

*  `data`
*  `build` (this is where your website will magically appear!)

`mkdir build data`

# Customising Loulou

Because Loulou uses [Bulmaswatch](https://jenil.github.io/bulmaswatch/), you can very easily change the colour scheme of your website.

Pick any theme you like from the **Bulmaswatch** website, download the corresponding *css* file and place it in the `css` folder. Don't forget to modify your `template_main.html` file accordingly.

Examples:

*  *Solar* (default theme)

![alt text](https://github.com/julien-blanchard/Loulou/blob/main/solar_loulou.png "Image")

*  *Slate*

![alt text](https://github.com/julien-blanchard/Loulou/blob/main/slate_loulou.png "Image")

*  *Journal*

![alt text](https://github.com/julien-blanchard/Loulou/blob/main/journal_loulou.png "Image")

*  *Nuclear*

![alt text](https://github.com/julien-blanchard/Loulou/blob/main/nuclear_loulou.png "Image")
