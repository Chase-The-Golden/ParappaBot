# ParappaBot
ParappaBot is a Discord bot that behaves like the PlayStation icon:

<img src = "https://image.api.playstation.com/cdn/UP9000/CUSA05289_00/pO3CdviiGzNCnHUoKcmE7rRERGR7jWT1.png" width=470>

In the game, Parappa the Rapper repeats his opponent's/master's rap by timing the buttons on the controller with the display. In some cases, he switches from first-person to second-person perspectives and vice-versa.
For example, if his opponent were to say:

`I don't know what to do, it's all because of you`

Parappa would rap back:

`*You* don't know what to do, it's all because of *me*`

ParappaBot behaves in that fashion; if an end user on Discord makes a post that calls the bot, the bot will post what the end user has typed up while switching up the perspectives.

It's a fun little gimmick to have in your channel if you're familiar with the rapping dog!

---
## Dev Note

**This is my first project in creating Discord bots *and* in using Python.**

To determine between subjects and objects in cases like "you" where ParappaBot must determine to switch it to "I" or "me", I used <a href="https://spacy.io/">SpaCy</a>, a natural language processor (NLP) for Python used for (but not limited to):

* Tokenization
* Classification
* Entity-recognition
* Chatbot development

From what I've read, SpaCy seems more useful for app development while another NLP, <a href="https://www.nltk.org/">Natural Language Toolkit</a> (NLTK), would be more for research development in natural language processors. Still I recommend looking into both of these as well as other NLPs for their usefulness in cases similar to ParappaBot's!
