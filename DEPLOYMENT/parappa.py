# This is a deployment build of the Parappa Bot for Discord
# It utilizes SpaCy: a natural language processor for which its purpose for this program is to identify subjects & objects in a sentence.
# More info on SpaCy here: https://spacy.io/
import spacy

from spacy.matcher import Matcher

# Standard SpaCy NLP & Matcher load in English model
nlp = spacy.load("en_core_web_sm")

# Matchers
contract = Matcher(nlp.vocab)   # Matcher for contractions e.g., "aren't" and "ain't"
matcher = Matcher(nlp.vocab)        # Matcher for pronoun-verbs

# Patterns for matching & retokenizing
### contractions
AintPattern = [{"LOWER" : "ai"}, {"LOWER" : {"IN" : ["n't", "nt"]}}]
ArentPattern = [{"LOWER" : "are"}, {"LOWER" : {"IN" : ["n't", "nt"]}}]
WasntPattern = [{"LOWER" : "was"}, {"LOWER" : {"IN" : ["n't", "nt"]}}]
WerentPattern = [{"LOWER" : "were"}, {"LOWER" : {"IN" : ["n't", "nt"]}}]

### pronoun-verbs (matcher)
##### Declarative
ImPattern = [{"LOWER" : "i"}, {"LOWER" : {"IN": ["'m", "m"]}}]
YourePattern = [{"LOWER" : "you"}, {"LOWER" : {"IN": ["'re", "re"]}}]
IAmPattern = [{"LOWER" : "i"}, {"LOWER" : "am"}]
YouArePattern = [{"LOWER": "you"}, {"LOWER" : "are"}]
IWasPattern = [{"LOWER" : "i"}, {"LOWER" : "was"}]
YouWerePattern = [{"LOWER" : "you"}, {"LOWER" : "were"}]
IAintPattern = [{"LOWER" : "i"}, {"LOWER" : {"REGEX" : "ain'?t"}}]
YouArentPattern = [{"LOWER" : "you"}, {"LOWER" : {"REGEX" : "aren'?t"}}]

##### Interrogative
AmIPattern = [{"LOWER" : "am"},  {"LOWER" : "i"}]
AreYouPattern = [{"LOWER" : "are"},  {"LOWER" : "you"}]
WasIPattern = [{"LOWER" : "was"},  {"LOWER" : "i"}]
WereYouPattern = [{"LOWER" : "were"},  {"LOWER" : "you"}]
AintIPattern = [{"LOWER" : {"REGEX" : "ain'?t"}}, {"LOWER" : "i"}]
ArentYouPattern = [{"LOWER" : {"REGEX" : "aren'?t"}}, {"LOWER" : "you"}]
WasntIPattern = [{"LOWER" : {"REGEX" : "wasn'?t"}}, {"LOWER" : "i"}]
WerentYouPattern = [{"LOWER" : {"REGEX" : "weren'?t"}}, {"LOWER" : "you"}]

# Adding to contractions
contract.add("Aint", [AintPattern])
contract.add("Arent", [ArentPattern])
contract.add("Wasnt", [WasntPattern])
contract.add("Werent", [WerentPattern])

# Adding to matcher
### Declarative
matcher.add("IAm", [ImPattern])
matcher.add("YouAre", [YourePattern])
matcher.add("IAmToo", [IAmPattern])
matcher.add("YouAreToo", [YouArePattern])
matcher.add("IWas", [IWasPattern])
matcher.add("YouWere", [YouWerePattern])
matcher.add("YouArent", [YouArentPattern])
matcher.add("IAint", [IAintPattern])

### Interrogative
matcher.add("AmI", [AmIPattern])
matcher.add("AreYou", [AreYouPattern])
matcher.add("WasI", [WasIPattern])
matcher.add("WereYou", [WereYouPattern])
matcher.add("AintI", [AintIPattern])
matcher.add("ArentYou", [ArentYouPattern])
matcher.add("WasntI", [WasntIPattern])
matcher.add("WerentYou", [WerentYouPattern])

# For future development; iterate through tuple list and switch with each tuple. Break on success.
'''
tupleList = [
    ("I am", "you are"),
    ("I'm", "you're"),
    ("Im", "youre"),
    ("I was", "you were"),
    ("I", "you"),
    ("me", "you"),
    ("my", "your"),
    ("mine", "yours")
]
'''

def repeat(message):
    rap = nlp(message)  # SpaCy's NLP of user input
    parappa = ''        # Parappa's line

    ''' Merged tokens using SpaCy's retokenize function
    Credit to Ines Motani https://stackoverflow.com/questions/56289487/is-there-a-way-to-turn-off-specific-built-in-tokenization-rules-in-spacy '''
    # Merged contractions
    with rap.retokenize() as retokenizer:
        for _, contrapt_start, contrapt_end in contract(rap):
            span = rap[contrapt_start:contrapt_end]
            retokenizer.merge(span)
    
    # Merged matcher
    with rap.retokenize() as retokenizer:
        for _, match_start, match_end in matcher(rap):
            span = rap[match_start:match_end]
            retokenizer.merge(span)

    # Add to "parappa" string depending on token
    for tokens in rap:
        # Declarative matchers
        if tokens.text.lower() == "i am":
            parappa += ("You are" if tokens.is_sent_start else "you are") + tokens.whitespace_
        elif tokens.text.lower() == "you are":
            parappa += "I am" + tokens.whitespace_
        elif tokens.text.lower() == "i ain't" or tokens.text.lower() == "i aint":
            parappa += ("You aren't" if tokens.is_sent_start else "you aren't") + tokens.whitespace_
        elif tokens.text.lower() == "you aren't" or tokens.text.lower() == "you arent":
            parappa += "I ain't" + tokens.whitespace_
        elif tokens.text.lower() == "i'm" or tokens.text.lower() == "im":
            parappa += ("You're" if tokens.is_sent_start else "you're") + tokens.whitespace_
        elif tokens.text.lower() == "you're" or tokens.text.lower() == "youre":
            parappa += "I'm" + tokens.whitespace_
        elif tokens.text.lower() == "i was":
            parappa += ("You were" if tokens.is_sent_start else "you were") + tokens.whitespace_
        elif tokens.text.lower() == "you were":
            parappa += "I was" + tokens.whitespace_
        # Interrogative matchers
        elif tokens.text.lower() == "am i":
            parappa += ("Are you" if tokens.is_sent_start else "are you") + tokens.whitespace_
        elif tokens.text.lower() == "are you":
            parappa += ("Am I" if tokens.is_sent_start else "am I") + tokens.whitespace_
        elif tokens.text.lower() == "was i":
            parappa += ("Were you" if tokens.is_sent_start else "were you") + tokens.whitespace_
        elif tokens.text.lower() == "were you":
            parappa += ("Was I" if tokens.is_sent_start else "was I") + tokens.whitespace_
        elif tokens.text.lower() == "ain't i" or tokens.text.lower() == "aint i":
            parappa += ("Aren't you" if tokens.is_sent_start else "aren't you") + tokens.whitespace_
        elif tokens.text.lower() == "aren't you" or tokens.text.lower() == "arent you":
            parappa += ("Ain't I" if tokens.is_sent_start else "ain't I") + tokens.whitespace_
        elif tokens.text.lower() == "wasn't i" or tokens.text.lower() == "wasnt i":
            parappa += ("Weren't you" if tokens.is_sent_start else "weren't you") + tokens.whitespace_
        elif tokens.text.lower() == "weren't you" or tokens.text.lower() == "werent you":
            parappa += ("Wasn't I" if tokens.is_sent_start else "wasn't I") + tokens.whitespace_
        # Individual matchers
        elif tokens.text.lower() == "i":
            parappa += ("You" if tokens.is_sent_start else "you") + tokens.whitespace_
        elif tokens.text.lower() == "me":
            parappa += ("You" if tokens.is_sent_start else "you") + tokens.whitespace_
        elif tokens.text.lower() == "you" and tokens.dep_ == "nsubj":   # You is the SUBJECT of the sentence
            parappa += "I" + tokens.whitespace_
        elif tokens.text.lower() == "you" and tokens.dep_ != "nsubj":   # You is NOT the SUBJECT of the sentence
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

#