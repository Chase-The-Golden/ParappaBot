# This is a test build and a proof of concept of the Parappa Bot for Discord
# It utilizes SpaCy: a natural language processor for which its purpose for this program is to identify subjects & objects in a sentence.
# More info on SpaCy here: https://spacy.io/
import spacy

from spacy.matcher import Matcher

# Standard SpaCy NLP & Matcher load in English model
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Patterns for matching & retokenizing
ImPattern = [{"LOWER" : "i"}, {"LOWER" : {"REGEX" : "[^a]'?m"}}]
YourePattern = [{"LOWER" : "you"}, {"LOWER" : {"REGEX" : "[^a]'?re"}}]
IAmPattern = [{"LOWER" : "i"}, {"LOWER" : "am"}]
YouArePattern = [{"LOWER": "you"}, {"LOWER" : "are"}]
IWasPattern = [{"LOWER" : "i"}, {"LOWER" : "was"}]
YouWerePattern = [{"LOWER" : "you"}, {"LOWER" : "were"}]
IWasntPattern = [{"LOWER" : "i"}, {"LOWER" : {"REGEX": "wasn'?t"}}]
YouWerentPattern = [{"LOWER" : "you"}, {"LOWER" : "weren'?t"}]

# Adding to matcher
matcher.add("IAm", [ImPattern])
matcher.add("YouAre", [YourePattern])
matcher.add("IAmToo", [IAmPattern])
matcher.add("YouAreToo", [YouArePattern])
matcher.add("IWas", [IWasPattern])
matcher.add("YouWere", [YouWerePattern])
matcher.add("IWasnt", [IWasntPattern])
matcher.add("YouWerent", [YouWerentPattern])

# For future development; iterate through tuple list and switch with each tuple. Break on success.
'''
tupleList = [
    ("I am", "you are"),
    ("I'm", "you're"),
    ("Im", "youre"),
    ("I was", "you were"),
    ("I wasn't", "you weren't"),
    ("I wasnt", "you werent"),
    ("I", "you"),
    ("me", "you"),
    ("my", "your"),
    ("mine", "yours")
]
'''

def repeat(message):
    rap = nlp(message)  # SpaCy's NLP of user input
    parappa = ''        # Parappa's line

    ''' Merged contractions using SpaCy's retokenize function
    Credit to Ines Motani https://stackoverflow.com/questions/56289487/is-there-a-way-to-turn-off-specific-built-in-tokenization-rules-in-spacy '''
    matches = matcher(rap)
    with rap.retokenize() as retokenizer:
        for match_id, match_start, match_end in matches:
            span = rap[match_start:match_end]
            retokenizer.merge(span)

    # Add to "parappa" string depending on token
    for tokens in rap:
        if tokens.text.lower() == "i am":
            parappa += ("You are" if tokens.is_sent_start else "you are") + tokens.whitespace_
        elif tokens.text.lower() == "you are":
            parappa += "I am" + tokens.whitespace_
        elif tokens.text.lower() == "i'm" or tokens.text.lower() == "im":
            parappa += ("You're" if tokens.is_sent_start else "you're") + tokens.whitespace_
        elif tokens.text.lower() == "you're" or tokens.text.lower() == "youre":
            parappa += "I'm" + tokens.whitespace_
        elif tokens.text.lower() == "i was":
            parappa += ("You were" if tokens.is_sent_start else "you were") + tokens.whitespace_
        elif tokens.text.lower() == "you were":
            parappa += "I was" + tokens.whitespace_
        elif tokens.text.lower() == "i wasn't" or tokens.text.lower() == "i wasnt":
            parappa += ("You weren't" if tokens.is_sent_start else "you weren't") + tokens.whitespace_
        elif tokens.text.lower() == "you weren't" or tokens.text.lower() == "you werent":
            parappa += "I wasn't" + tokens.whitespace_
        elif tokens.text.lower() == "i":
            parappa += ("You" if tokens.is_sent_start else "you") + tokens.whitespace_
        elif tokens.text.lower() == "me":
            parappa += ("You" if tokens.is_sent_start else "you") + tokens.whitespace_
        elif tokens.text.lower() == "you" and tokens.dep_ == "nsubj":
            parappa += "I" + tokens.whitespace_
        elif tokens.text.lower() == "you" and tokens.dep_ != "nsubj":
            parappa += ("Me" if tokens.is_sent_start else "me") + tokens.whitespace_
        elif tokens.text.lower() == "my":
            parappa += ("Your" if tokens.is_sent_start else "your") + tokens.whitespace_
        elif tokens.text.lower() == "your":
            parappa += ("My" if tokens.is_sent_start else "my") + tokens.whitespace_
        elif tokens.text.lower() == "mine":
            parappa += ("Yours" if tokens.is_sent_start else "yours") + tokens.whitespace_
        elif tokens.text.lower() == "yours":
            parappa += ("Mine" if tokens.is_sent_start else "mine") + tokens.whitespace_
        else:
            parappa += tokens.text_with_ws
            
    # print (parappa) # DEBUG: Print parappa's message in the terminal
    return parappa