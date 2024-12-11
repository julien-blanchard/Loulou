---
title: "Make your websites prettier with MVP.CSS"
date: 2021-12-04
summary: "I was browsing through recent comments on Hacker News when I stumbled upon a conversation around minimalistic web design"
draft: false
---

<script src="https://cdn.counter.dev/script.js" data-id="205ad799-38b0-4d9a-ac65-2fdf615ff871" data-utcoffset="0"></script>

A couple of weeks ago, as I was browsing through recent comments on **Hacker News** when I stumbled upon a conversation around [minimalistic web design](https://news.ycombinator.com/item?id=22681270). As my HTML and CSS skills are quite limited, I thought I might take a look at some of the resources that were being shared there and see how they could benefit my own work. 

## Make your ugly HTML files prettier

So, what is MVP.css? According to its author, [Andy Brewer](https://andybrewer.github.io/mvp/), it is a *"a minimalist stylesheet for HTML elements"*. The official website itself is both simple and elegant, with the following brilliant one-liner at the top of the page:

> *"No class names, no frameworks, just semantic HTML and you're done."*

As a matter of fact, all you need to do is add this one line of HTML code between your `<head></head>` tags:

```html
<link rel="stylesheet" href="https://unpkg.com/mvp.css">
```

And that's it. You need a button? Well then you won't need to read through an entire documentation and learn custom semantics such as ~~`<button type="button" class="btn btn-primary btn-lg">I can see what you're doing here Bootstrap</button>`~~ .

Just add a regular HTML button tag to your code:

```html
<button>MVP.CSS is great</button>
```

And this is what you should get:

![alt text](/images/mvp01.png "Image")

## Hey, I'm into Data Analytics / Science / Engineering, not Web Development!

Fair point. That being said, it is still quite likely that you might have to work with HTML files at some point. Especially if you ~~have to~~ wish to share some insights with leadership, or with some people that you work with. 

*   Automated email reports (Check out my article on how to send a Pandas dataframe by email)
*   Dashboards (See the article on **VegaLite.js**)
*   PDF reports
*   [ **July 2022 update** ] PyScript aka Python in the browser

## Examples

Say we have been tasked with building a simple report, that will have to be sent by email on every Monday. The report will contain a title, a couple of links, a Pandas dataframe in HTML format, and a couple of charts.

Being very professional, but not very competent in HTML or CSS, we're probably going to end up writing something along those lines:

```html
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="https://unpkg.com/mvp.css">
  <title></title>
</head>

<body>
  <main>
    <header>
      <h1>This is a weekly report</h1>
      <p>Hey check out this report, it's cool!</p>
      <h3>You will want to click those buttons</h3> 
      <p> <a href="#"><i>Hey dude, I'm a link</i></a> <a href="#"><i>Me too, I'm also a link!</i></a> </p>
    </header>
    <header>
      <h3>We have some very serious looking tables</h3>
      <table>
        <tr>
          <th>Name</th>
          <th>Role</th>
          <th>Sales</th>
          <th>Percentage</th>
        </tr>
        <tr>
          <td>Julien</td>
          <td>Data</td>
          <td>60</td>
          <td>12%</td>
        </tr>
        <tr>
          <td>Juju</td>
          <td>Analyst</td>
          <td>45</td>
          <td>8%</td>
        </tr>
      </table>
    </header>
  </main>
</body>
``` 

![alt text](/images/mvp02.png "Image")

Without using any stylesheet, our report will look like it's coming straight from the late 90s. Now at this point, we could either try and learn some CSS, or learn a framework like **Bootstrap**, **Tailwind**, or **Bulma**.

But what if we simply added this one line of HTML code, and reloaded our page?

```html
<link rel="stylesheet" href="https://unpkg.com/mvp.css">
```

![alt text](/images/mvp03.png "Image")

Wow! We now have a completely different report, that we can either attach to an email, convert to PDF format, etc.. And all it took was to load **MVP.CSS**. No new class name, etc.. Plus, it's mobile friendly. One little caveat though, is that you might want to save the `.css` file locally, as the loading times can otherwise vary.

If you are interested and want to know more, **MVP.CSS** currently [supports a lot of HTML tags](https://andybrewer.github.io/mvp/#docs) and I strongly recommend you to take a look at the various examples that are available on Andy's website.
