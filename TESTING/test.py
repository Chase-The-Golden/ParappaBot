# This is a test build and a proof of concept of the Parappa Bot for Discord
# It utilizes SpaCy: a natural language processor for which its purpose for this program is to identify subjects & objects in a sentence.
# More info on SpaCy here: https://spacy.io/
import spacy

from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

# Matchers
contractions = Matcher(nlp.vocab)   # Matcher for contractions e.g., "aren't" and "ain't"
matcher = Matcher(nlp.vocab)        # Matcher for pronoun-verbs

# Patterns for matching & retokenizing
### contractions
AintPattern = [{"LOWER" : "ai"}, {"LOWER" : {"IN" : ["n't", "nt"]}}]
ArentPattern = [{"LOWER" : "are"}, {"LOWER" : {"IN" : ["n't", "nt"]}}]

### pronoun-verbs (matcher)
ImPattern = [{"LOWER" : "i"}, {"LOWER" : {"IN": ["'m", "m"]}}]
YourePattern = [{"LOWER" : "you"}, {"LOWER" : {"IN": ["'re", "re"]}}]
IAmPattern = [{"LOWER" : "i"}, {"LOWER" : "am"}]
YouAre2Pattern = [{"LOWER" : "you"}, {"LOWER" : "are"}]
IAintPattern = [{"LOWER" : "i"}, {"LOWER" : {"REGEX" : "ain'?t"}}]
YouAre3Pattern = [{"LOWER" : "you"}, {"LOWER" : {"REGEX" : "aren'?t"}}]

# contractions
contractions.add("Aint", [AintPattern])
contractions.add("Arent", [ArentPattern])

# matcher
matcher.add("IAm", [ImPattern])
matcher.add("YouAre", [YourePattern])
matcher.add("IAmToo", [IAmPattern])
matcher.add("YouAreToo", [YouAre2Pattern])
matcher.add("IAint", [IAintPattern])
matcher.add("YouAreThree", [YouAre3Pattern])

tupleList = [
    ("I am", "you are"),
    ("I ain't", "you aren't"),
    ("I aint", "you arent"),
    ("I'm", "you're"),
    ("Im", "youre"),
    ("I", "you"),
    ("me", "you"),
    ("my", "your"),
    ("mine", "yours")
]

# Infinite loop
isLoop = True
while isLoop == True:
    prompt = input("Input: ")  # User input, no text prompt present; just type your message
    rap = nlp(prompt)   # SpaCy's NLP of user input
    parappa = ''
    
    ''' Merged tokens using SpaCy's retokenize function
    Credit to Ines Motani https://stackoverflow.com/questions/56289487/is-there-a-way-to-turn-off-specific-built-in-tokenization-rules-in-spacy '''
    # Merged contractions
    with rap.retokenize() as retokenizer:
        for contrap_id, contrapt_start, contrapt_end in contractions(rap):
            span = rap[contrapt_start:contrapt_end]
            retokenizer.merge(span)
    
    # Merged matcher
    with rap.retokenize() as retokenizer:
        for match_id, match_start, match_end in matcher(rap):
            span = rap[match_start:match_end]
            retokenizer.merge(span)

    # Add to "parappa" string depending on token
    for tokens in rap:
        replaced = False
        for (x, y) in tupleList:
            if tokens.text.lower() == x.lower():
                parappa += (y.capitalize() if tokens.is_sent_start else y) + tokens.whitespace_
                replaced = True
            elif tokens.text.lower() == y.lower():
                parappa += (x.capitalize() if tokens.is_sent_start else x) + tokens.whitespace_
                replaced = True

            if replaced == True:
                break

        if replaced == False:
            parappa += tokens.text_with_ws
        # if tokens.text.lower() == "i am":
        #     parappa += ("You are" if tokens.is_sent_start else "you are") + tokens.whitespace_
        # elif tokens.text.lower() == "you are":
        #     parappa += "I am" + tokens.whitespace_
        # elif tokens.text.lower() == "i ain't" or tokens.text.lower() == "i aint":
        #     parappa += ("You aren't" if tokens.is_sent_start else "you aren't") + tokens.whitespace_
        # elif tokens.text.lower() == "you aren't" or tokens.text.lower() == "you arent":
        #     parappa += "I ain't" + tokens.whitespace_
        # elif tokens.text.lower() == "i'm" or tokens.text.lower() == "im":
        #     parappa += ("You're" if tokens.is_sent_start else "you're") + tokens.whitespace_
        # elif tokens.text.lower() == "you're" or tokens.text.lower() == "youre":
        #     parappa += "I'm" + tokens.whitespace_
        # elif tokens.text.lower() == "i":
        #     parappa += ("You" if tokens.is_sent_start else "you") + tokens.whitespace_
        # elif tokens.text.lower() == "me":
        #     parappa += ("You" if tokens.is_sent_start else "you") + tokens.whitespace_
        # elif tokens.text.lower() == "you" and tokens.dep_ == "nsubj":
        #     parappa += "I" + tokens.whitespace_
        # elif tokens.text.lower() == "you".lower() and tokens.dep_ != "nsubj":
        #     parappa += ("Me" if tokens.is_sent_start else "me") + tokens.whitespace_
        # elif tokens.text.lower() == "my":
        #     parappa += ("Your" if tokens.is_sent_start else "your") + tokens.whitespace_
        # elif tokens.text.lower() == "your":
        #     parappa += ("My" if tokens.is_sent_start else "my") + tokens.whitespace_
        # elif tokens.text.lower() == "mine":
        #     parappa += ("Yours" if tokens.is_sent_start else "yours") + tokens.whitespace_
        # elif tokens.text.lower() == "yours":
        #     parappa += ("Mine" if tokens.is_sent_start else "mine") + tokens.whitespace_
        # else:
        #     parappa += tokens.text_with_ws

        # print("Token: " + tokens.text)    # DEBUG: Print each token for diagnosis
        
    print ("Output: " + parappa) # Return parappa's message

    # Exit loop
    if prompt.lower() == "quit":
        isLoop = False