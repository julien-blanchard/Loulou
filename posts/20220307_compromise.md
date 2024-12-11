---
{
"title":"Basic in-browser text processing using Compromise.js",
"date":"2022-03-07",
"summary":"Though JavaScript might not be as obvious a choice as Python when it comes to NLP libraries, its ecosystem actually features some highly performing text processing packages",
"tags":["nlp","javascript"],
"featured":false,
"readTime":"9 minutes"
}
---

Though JavaScript might not be as obvious a choice as Python when it comes to *Natural Language Processing* libraries, its ecosystem actually features some highly performing text processing packages. And this actually makes perfect sense, as such dependencies are very much needed to build mobile or web based applications such as chatbots for instance.

## Finding the right tool for the job

Over the past few months, I have experimented a bit with the following *Node* packages:

*  [Natural.js](http://naturalnode.github.io/natural/): a very comprehensive module that I found quite remminiscent of NLTK in many ways. From what I have seen, its [TD-IDF vectorizer](http://naturalnode.github.io/natural/tfidf.html) seems particularly efficient.
*  [winNLP.js](https://winkjs.org/wink-nlp/): I absolutely love this library. If you need any sort of convincing, simply take a look at its `.markup()` method and what it can do.
*  [reText.js](https://github.com/retextjs/retext): I have mostly used this popular package for the set of extra tools (plugins) it provides. Be sure you check out the spelling corrector and repeated words plugins.

However, most of these solutions were primarily designed to work on *Node.js*, and therefore require a local or server *npm* installation. That being said, these modules and their dependancies can be turned into static assets using either [Webpack](https://webpack.js.org/) or [Browserify](https://browserify.org/), but as I have encountered some weird compatibility issues when using either of these two module bundlers we won't be including them in this article.

Anyway, I was recently going through some random [ObservableHQ notebooks](https://observablehq.com/explore) when I came across a *Natural Language Processing* tool for JavaScript that I had never heard of. Named [Compromise.js](https://github.com/spencermountain/compromise), this fairly recent library offers a client-side package that can be loaded directly from the [Unpkg](https://unpkg.com/) CDN.

```html
<script src="https://unpkg.com/compromise"></script>
```

## Please help us, Pico.css

Before anything else, we want to make sure that we have a webpage and a text area form, as well as some basic *HTML* elements and their corresponding unique `id=` attribute that will come in handy when writing our JavaScript functions. We particularly need:

1.  A simple `<form>` element
2.  Two `<textarea>` blank spaces (a first one for the text input, and a second one for the transformed text output)
3.  A dropdown menu, made of several distinct `<option>` elements, to allow our users to pick which *NLP* task they would like to perform.
4.  A couple of `<button>` so that we can capture what a user might type into our first `<textarea>`, but also reset this user input when needed.

All of the above shouldn't be too complicated, and we can just paste the code below into a `.html` file.

```html
<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="dark">

<head>
  <meta charset="utf-8">
  <script src="https://unpkg.com/compromise"></script>
  <title>NLP with Compromise.js</title>
</head>

<body>
  <main class="container">
    <div class="headings">
    <h2>Basic text processing using <a href="https://github.com/spencermountain/compromise/" target="_blank">Compromise.js</a></h2>
    <h3>An in-browser rule-based parser</h3>
    </div>
    <br>
    <form>
      <label>Enter your text below:</label>
      <textarea type="text" rows=4 id="text_input" placeholder="Make sure that the text that you paste here is in English."></textarea>
      <label>Output:</label>
      <textarea type="text" rows=4 id="text_output" placeholder="Output."></textarea>
      <select id="choice">
        <option>To plural form</option>
        <option>To negative form</option>
        <option>To future tense</option>
        <option>To past tense</option>
        <option>To POS tags</option>
      </select>
      <a href="#" role="button" onclick="getNLP()">Process</a>
      <a href="#" role="button" onclick="clearText()">Clear</a>
    </form>
  </main>
</body>

</html>
```

![alt text](/images/compromise01.png "Image")

Well, let's be honest, that doesn't look too good. I mean it would probably have looked halfway decent in the late 90s, but definitely not today. On the other hand, we're data people, not web developers right?

Without changing any tag or attribute, we can however make our form look much better by using a minimalist *CSS* framework. My favorite ones currently are:

*  [MVP.css](https://andybrewer.github.io/mvp/)
*  [Milligram.css](https://milligram.io/)
*  [Pico.css](https://picocss.com/)

We're going to go with *Pico.css* today, and to make our text parser look prettier all we have to do is paste the following line of code between the `<head></head>` elements in our `.html` file:

```html
<link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css">
```

When we hit the F5 button, we're now greeted by this much better looking webpage.

![alt text](/images/compromise02.png "Image")

## So how does Compromise.js work?

According to [its author](https://observablehq.com/@spencermountain/compromise-justification),

>  "*Compromise.js is not the most accurate, or most clever nlp toolkit. It is though, pretty fun to use."*

I quite like that approach. It focuses on getting the work done and keeping things simple, which is exactly what we need for this little project.

If you have ever used [spaCy](https://spacy.io/), a powerful *NLP* library for Python, then the good news is that you are going to find yourself in familiar territory. But dont't worry if you haven't, as learning the ropes of *Compromise.js* isn't really complicated. Plus, the official documentation does a pretty good job at showcasing all the basic functionalities and how to implement them quickly.

We can start by adding the following two `<script></script>` tags between our `<head></head>` elements:

```html
<script src="https://unpkg.com/compromise"></script>
<script type="text/javascript" src="script.js"></script>
```

The first of these two lines simply calls the *Compromise.js* package, while the second one calls a `script.js` file that we're going to create and place in the same folder as our `index.html` page.

Remember earlier on when I mentioned *spaCy*? Importing this library in a Python environment and processing some chunk of text is as easy as this:

```python
import spacy
nlp = spacy.load("en_core_web_sm")
text = "Hi my name is Julien."
doc = nlp(text)
```

From there, we can then tokenize our sentence and do all sort of cool things. But let's go back to our `script.js` file and see how this would work using *Compromise.js*:

```javascript
let text = "Hi my name is Julien."
let doc = nlp(text);
```

So, pretty much the same, right? If you're working in *Node.js* though, please note that you'll have to import the package first: `import nlp from "compromise"`.

Back to the `doc` variable that we defined earlier on, let's have a look at some of the methods that we might want to use for our text parser project:
*  `doc.verbs().toPastTense()` will change all verbs within the sentence to the past tense 
*  `doc.verbs().toPastTense()` does the same, to the future tense this time
*  `doc.verbs().toNegative()` turns a sentence to its negative form
*  `doc.contractions().expand()` changes contracted verbs to their full form
*  `doc.numbers().add()` magically adds a given numeric value to any number in text format. For instance `.add(2)` will change *"It's one o'clock"* to *"it's three o'clock"* 
*  `doc.numbers().minus()` does the same, but for substractions this time
*  `doc.nouns().toPlural()` changes any nouns to their plural form

You will find a full list of supported methods [here](https://github.com/spencermountain/compromise#api).

No matter what method we pick, the processed text string can be easily visualised by appending `.text()` to the `doc` variable. So for instance, if we want to get the full form for each verb within a given sentence instead of their contracted form, we can simply write:

```javascript
let doc = nlp("I'm playing with JavaScript and that's cool.")
doc.contractions().expand()
console.log(doc.text())
```

![alt text](/images/compromise03.png "Image")

By the way, I'm using [PlayCode](https://playcode.io/) to write this article, an online *JavaScript* playground that allows its users to import any *npm* package without having to do any local install. 

## A simple text parser 

To be able to capture what our users will be typing in the upper `<textarea>` element, we can write a simple `getText()` function that returns a single string value named `user_input`:

```javascript
const getText = () => {
  let user_input = document.getElementById("text_input").value;
  return user_input;
}
```

Next comes a function that will determine what type of method gets applied to the user's input very much resembles the `getText()` function we just wrote:

```javascript
const getChoice = () => {
  let user_choice = document.getElementById("choice").value;
  return user_choice;
}
```

The `clearText()` function too, is as simple as it gets, and simply changes the value of each `<textarea>` element to an empty string:

```javascript
const clearText = () => {
  document.getElementById("text_input").value = "";
  document.getElementById("text_output").value = "";
};
```

All that is left to do at this point, is write a fourth function that captures the user's input as well as the text processing method they have chosen, and uses some simple conditional statements to output the result into the lower `<textarea>` element: 

```javascript
const getNLP = () => {
  let tokens = getText();
  let choice = getChoice();
  let doc = nlp(tokens);
  if (choice == "To plural form") {
    doc.nouns().toPlural();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To negative form") {
    doc.verbs().toNegative();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To future tense") {
    doc.verbs().toFutureTense();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To past tense") {
    doc.verbs().toPastTense();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To POS tags") {
    doc.compute("penn");
    let tokens = doc.json()[0].terms;
    tags = tokens.map(term => [ term.text, term.penn]);
    let result = ""
    for (let tag of tags) {
        result += (tag.join(": ") + " / ");
    }
    document.getElementById("text_output").value = result.slice(0,-2);
  }
};
```

Now there is one thing that we didn't discuss earlier but that you have probably spotted in the code above, which is how *Compromise.js*'s *Part-of-speech tagger* works. By passing a parameter to the `doc.compute()` method, we tell *Compromise.js* that we want to use the [Penn Treebank POS tagger](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html), a popular and reliable tagset that was developped in the 1990s at the [university of Pennsylvania](https://dl.acm.org/doi/10.5555/972470.972475).

```javascript
let text = "Hi my name is Julien."
let doc = nlp(text);
doc.compute("penn");
let tokens = doc.json()[0].terms;
console.log(tokens);
```

![alt text](/images/compromise04.png "Image")

We get a *JSON* object that contains a bunch of information about each token within the sentence that was passed through *Compromise.js*'s parser. What we really need though, is simply the token in its original form, and its associated *POS tag*.

We can easily get this by looping through the *JSON* variable, using *JavaScript*'s `.map()` method to access the `.text` and `.penn` values only, and then joining the resulting array with the help of a simple `.join()` method:

```javascript
tags = tokens.map(term => [ term.text, term.penn]);
let result = "";
for (let tag of tags) {
        result += (tag.join(": ") + " / ");
    }
console.log(result);
```

![alt text](/images/compromise05.png "Image")

Now that this is clear, let's go through a couple of scenarios together, just to make sure everything's working alright!

*  If we type in a random assertive sentence, select *To negative form*, we get the following result:

![alt text](/images/compromise06.png "Image")

*  Next, we can process another sentence, this time selecting our POS tagger:

![alt text](/images/compromise07.png "Image")

Pretty neat, eh?

## Putting everything together

Below is the full JavaScript code for our final text parser. I hope you enjoyed this article!

```javascript
const getNLP = () => {
  let tokens = getText();
  let choice = getChoice();
  let doc = nlp(tokens);
  if (choice == "To plural form") {
    doc.nouns().toPlural();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To negative form") {
    doc.verbs().toNegative();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To future tense") {
    doc.verbs().toFutureTense();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To past tense") {
    doc.verbs().toPastTense();
    document.getElementById("text_output").value = doc.text();
  }
  else if (choice == "To POS tags") {
    doc.compute("penn");
    let tokens = doc.json()[0].terms;
    tags = tokens.map(term => [ term.text, term.penn]);
    let result = ""
    for (let tag of tags) {
        result += (tag.join(": ") + " / ");
    }
    document.getElementById("text_output").value = result.slice(0,-2);
  }
};

const getText = () => {
  let user_input = document.getElementById("text_input").value;
  return user_input;
};

const getChoice = () => {
  let user_choice = document.getElementById("choice").value;
  return user_choice;
}

// Clearing the text input area
const clearText = () => {
  document.getElementById("text_input").value = "";
  document.getElementById("text_output").value = "";
};
```