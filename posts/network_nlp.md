---
title: "Using POS tags to draw simple network graphs"
date: 2024-10-27
summary: "Another week, another article inspired by some project I've recently been involved in at work"
draft: false
---

<script src="https://cdn.counter.dev/script.js" data-id="205ad799-38b0-4d9a-ac65-2fdf615ff871" data-utcoffset="0"></script>

*An example of what we’ll be discussing in this article*

![alt text](/images/network_nlp08.png "Image")

Another week, another article inspired by some project I've recently been involved in at work.

We saw in a [recent article](https://blanchardjulien.com/posts/networkplots/) how to utilise [**NetworkX**](https://networkx.org/) or [**AnyChart**](https://www.anychart.com/) to draw basic network graphs. As our purpose back then was to focus on understanding how to create nodes and output a simple chart, we used some synthetic data and didn't really try to solve any concrete problem.

Our plan for today is to create a simple *NLP* prep-processing workflow that can be used to boost up the exploration of any text-based dataset that you might want to work with.

# Fraud, fraud everywhere!

So what have I been working on lately you may wonder?

Long story short, let's just say that we have access to a significant amount of text data related to motor incidents. So far, nothing to write home about you might think. What's particularly interesting in this scenario is that each text snippet is indexed against a unique fraud score ranging from zero to one.

No matter what industry you are working in, there's a high chance that as a data practitioner you will be ask to jump in and perform some investigation. Each year, fraud costs all companies around the world a [significant amount of money](https://hn.algolia.com/?q=fraud+cost). Being able to proactively identify fraudsters and understand their patterns has been a highly sought-after skill everywhere I have worked in my career.

# Context is everything

Don't get me wrong: we're not going to do anything that's even remotely revolutionary. You'll easily find across the web tons of articles similar to this one. I still believe that this approach allows for an overview of potential clusters of interest and how they are related to one another.

But before we start having fun with the [**spaCy**](https://spacy.io/) library, what do we mean by *"context"*?

Alright, this is what the first paragraphs of the [**Wikipedia**](https://en.wikipedia.org/wiki/Fraud) entry for *"Fraud"* look like:

![alt text](/images/network_nlp01.png "Image")

```python
corpus: str = '''
"Phony" redirects here. For the Vocaloid song, see Phony (song). In law, fraud is intentional deception to secure unfair or unlawful gain, or to deprive a victim of a legal right. Fraud can violate civil law (e.g., a fraud victim may sue the fraud perpetrator to avoid the fraud or recover monetary compensation) or criminal law (e.g., a fraud perpetrator may be prosecuted and imprisoned by governmental authorities), or it may cause no loss of money, property, or legal right but still be an element of another civil or criminal wrong. The purpose of fraud may be monetary gain or other benefits, for example by obtaining a passport, travel document, or driver's license, or mortgage fraud, where the perpetrator may attempt to qualify for a mortgage by way of false statements.
'''
```

Well let's consider that *"fraud"* term for a moment. See how each iteration of *"fraud"* is preceded and followed by some other terms? It's those words that we want to retrieve.

A simple script should do that for us:

```python
def getContext(term: str,n_tokens: int) -> None:
    tokens: List[str] = [c.lower() for c in corpus.split(" ")]
    for idx, token in enumerate(tokens):
        if token == term.lower():
            context: List[str] = [tokens[i] for i in range(idx - n_tokens, idx + n_tokens)]
            output: str = f"Context for {term.upper()} (line {str(idx)}):\n\t{' | '.join(context)}"
            print(output)

getContext("fraud",3)
```

![alt text](/images/network_nlp02.png "Image")

Yes, our very primitive tokenizer simply assumes that all terms are separated by a white space. But the `getContext()` function still did a pretty good job at returning the contextual terms that we were looking for.

# Who let the dogs out? 

As you can imagine we won't be working with that text data that I briefly mentioned a little while ago.

Instead, why don't head over to [**Project Gutenberg**](https://www.gutenberg.org/) and see what we can find there?

I've always been a big fan of [**Arthur Conan Doyle**](https://en.wikipedia.org/wiki/Arthur_Conan_Doyle)'s [**The Hound of the Baskervilles**](https://www.gutenberg.org/ebooks/2852), and this short novel is a perfect match for what we're trying to do here.

Let's download a digital copy in *txt* format and save it to a variable:

```python
with open("baskervilles.txt", "r") as text_file:
    corpus: str = text_file.read()

print(corpus[:90])
```

![alt text](/images/network_nlp03.png "Image")

# Verbs == action

We'll be using [**spaCy**](https://spacy.io/) as our main *NLP* library. Please note that we could have picked [**NLTK**](https://www.nltk.org/) instead of **spaCy** and obtained the same results. These are both fantastic projects with very slightly different purposes. As we might want to create a production-ready data pipeline, using **spaCy** simply allows for a bit more flexibility in that regard.

Remember that very naive tokenizer we wrote a couple of minutes ago? Unsurprisingly, we can now get a much better output with a lot less code:

```python
import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

doc = nlp(corpus)
```

Besides, we're now able to choose what specific part-of-speech tag we want to retrieve. So let's rewrite our `getContext()` function and see what *verbs* it returns:

```python
def getContext(term: str,n_tokens: int) -> None:
    for idx, token in enumerate(doc):
        if token.text == term:
            contextual_verbs: List[str] = [t.text for t in doc[idx-n_tokens : idx+n_tokens] if t.pos_ == "VERB"]
            output: str = f"Context for {term.upper()} (line {str(idx)}):\n\t{' | '.join(contextual_verbs)}"
            print(output)

getContext("Holmes",5)
```

![alt text](/images/network_nlp05.png "Image")

Of course, there may cases where the term entered (here, *"Holmes"*) isn't preceded or followed by any verb. Let's get rid of these. Given the size of the corpus that shouldn't affect the output of this exercise though.

Now as we'll be doing some basic aggregation in a little while, we probably want to retrieve the *lemma* of each term instead of its full form. Consider the following three terms: `have, had, having`. It makes a lot more sense to transform them into their *lemma* `have` so that we can count the occurences of any lexeme in a more effective manner.

```python
def getContext(term: str,n_tokens: int) -> None:
    for idx, token in enumerate(doc):
        if token.text == term:
            contextual_verbs: List[str] = [t.lemma_ for t in doc[idx-n_tokens : idx+n_tokens] if t.pos_ == "VERB"]
            if len(contextual_verbs) != 0:
                output: str = f"Context for {term.upper()} (line {str(idx)}):\n\t{' | '.join(contextual_verbs)}"
                print(output)

getContext("Watson",10)
```

![alt text](/images/network_nlp06.png "Image")

#  A more structured approach

Now that we have a better understanding of what we're trying to achieve, our next logical step is to speed up our game by:

*  Obtaining a list of the key characters present in the novel for us to loop through
*  Save the output of our `` function as a [**Pandas**](https://pandas.pydata.org/) *DataFrame* object

```python
characters: List[str] = [
    "Holmes",
    "Watson",
    "Hugo",
    "Charles",
    "Henry",
    "Mortimer",
    "Selden",
    "John",
    "Elisa",
    "Jack",
    "Beryl",
    "Frankland",
]

data: Dict[str, List[str]] = {
    "Characters": [],
    "Verbs": []
}

def getContext(term: str,n_tokens: int) -> None:
    for idx, token in enumerate(doc):
        if token.text in characters:
            contextual_verbs: List[str] = [t.lemma_ for t in doc[idx-n_tokens : idx+n_tokens] if t.pos_ == "VERB"]
            if len(contextual_verbs) != 0:
                for verb in contextual_verbs:
                    data["Characters"].append(token.text)
                    data["Verbs"].append(verb)

getContext("Watson",10)
```

Remember earlier when we said we would perform some aggregation on the data we would process? Let's keep things simple by counting the number of associated terms for each character, and removing each of these terms that has less than 3 occurences:

```python
def prepareData(data):
    dframe: pd.DataFrame = (
        pd
        .DataFrame(data)
        .groupby(["Characters","Verbs"])[["Verbs"]]
        .count()
        .rename(columns={"Verbs":"Volume"})
        .reset_index(drop=False)
        .query("Volume >= 3")
        .sort_values(["Characters","Volume"], ascending=False)
    )
    return dframe

df: pd.DataFrame = prepareData(data_struct)
df.head(10)
```

![alt text](/images/network_nlp07.png "Image")

We're pretty much done at this point, and all we have to do is reuse the simple plotting functions that we wrote a few months ago:

```python
def getNetworkPlot(data,serie1,serie2,serie3,title):
    G = nx.from_pandas_edgelist(data, serie1, serie2, edge_attr=True)
    edgelist = nx.to_edgelist(G)

    colors = [i/len(G.nodes) for i in range(len(G.nodes))]

    plt.figure(figsize=(15,9))
    nx.draw(
        G,
        with_labels = True,
        node_size = [v * 200 for v in dict(G.degree()).values()],
        #width_size = [e[2][serie3] / 500 for e in edgelist],
        font_size = 12,
        node_color = colors,
        cmap = "Pastel1"
    )
    plt.title(title)
    plt.show()

getNetworkPlot(df,"Characters","Verbs","Volume","")
``` 

![alt text](/images/network_nlp08.png "Image")

As you would have probably guessed, *Sherlock Holmes* really is the central character of the story. Common to all characters are what we'd best describe as *"communication"* verbs: *"say", "tell", "ask"*. This makes sense from a narrative perspective I guess, as the story progresses through *Holmes* and *Watson* interactives with the inhabitants of *Dartmoor*.

But what you'll also notice is that each character is associated to their own unique set of verbs. In this specific case we might want to interpret these as personality traits, and running the same function on a potentially fraud-ridden corpus should provide you with some interesting insights.
