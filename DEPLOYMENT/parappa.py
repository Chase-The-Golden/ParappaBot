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
YouArePattern = [{"LOWER" : "you"}, {"LOWER" : "are"}]
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
matcher.add("Im", [ImPattern])
matcher.add("Youre", [YourePattern])
matcher.add("IAm", [IAmPattern])
matcher.add("YouAre", [YouArePattern])
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

# Iterate through tuple list and switch with each tuple. Break on success.
tupleList = [
    ("I am", "you are"),
    ("I ain't", "you aren't"),
    ("I aint", "you arent"),
    ("I'm", "you're"),
    ("Im", "youre"),
    ("I was", "you were"),
    ("am I", "are you"),
    ("was I", "were you"),
    ("ain't I", "aren't you"),
    ("aint I", "arent you"),
    ("wasn't I", "weren't you"),
    ("wasnt I", "werent you"),
    ("my", "your"),
    ("mine", "yours")
]

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
        # Looping through tuple list for compacting code
        replaced = False    # Bool check to see if a token has been replaced

        # Accessing x and y values from list of tuples to match tokens with, line 66
        for (x, y) in tupleList:
            if tokens.text.lower() == x.lower():
                parappa += ((y[0].upper() + y[1:]) if tokens.is_sent_start else y) + tokens.whitespace_
                replaced = True
            elif tokens.text.lower() == y.lower():
                parappa += ((x[0].upper() + x[1:]) if tokens.is_sent_start else x) + tokens.whitespace_
                replaced = True

            # break from for loop if token is "replaced" to save runtime
            if replaced == True:
                break

        # On no replacements done, check special case
        if replaced == False:
            # SPECIAL CASE: Determining if you is the subject or object of the sentence
            if tokens.text.lower() == "you" and tokens.dep_ == "nsubj":
                parappa += "I" + tokens.whitespace_
            elif tokens.text.lower() == "you" and tokens.dep_ != "nsubj":
                parappa += ("Me" if tokens.is_sent_start else "me") + tokens.whitespace_
            elif tokens.text.lower() == "i":
                parappa += ("You" if tokens.is_sent_start else "you") + tokens.whitespace_
            elif tokens.text.lower() == "me":
                parappa += ("You" if tokens.is_sent_start else "you") + tokens.whitespace_
            # NON-SPECIAL CASE: Simply add token if all else fails
            else:
                parappa += tokens.text_with_ws

    # print (parappa) # DEBUG: Print parappa's message in the terminal
    return parappa