import config as config
import string

# Splits the text input into individual words. Removes ALL punctuation
def tokenise(s):
    s = s.lower()
    s = s.decode('unicode_escape').encode('ascii','ignore');
    tokens = []
    for item in string.punctuation:
        s = s.replace(item, " ")

    word = ""
    for char in s:
        if char != " ":
            word += char
        else:
            if word.replace(" ", "") != "":
                tokens.append(word)
            word = ""
    return tokens

# Removes useless words
def filterWords(tokenList):
    tokens = []
    for item in tokenList:
        if not(item in config.words_to_ignore):
            tokens.append(item)
    return tokens

# ONLY USE THIS FUNCTION when using this module in other pythno scripts. For safety.
def toke(s):
    tokens = tokenise(s)
    return filterWords(tokens)
