#!/usr/bin/python

import re

from nltk.tokenize import WhitespaceTokenizer

import contractions
import stopwords
# TO DO - convert unicode to ascii
def convert_unicode(text):
    pass

# TO DO - remove links
def remove_links(text):
    pass

# TO DO - remove emails
def remove_emails(text):
    return re.sub(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", "", text)

def remove_digits(text):
    return re.sub(r"[0-9]", " ", text)

def remove_stopwords(list):
    sw = stopwords.stopwords
    no_stopwords = []
    for each in list:
        if each not in sw:
            no_stopwords.append(each)
    return no_stopwords

def convert_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text)

# strip whitespace from the start and end of the "line" and convert 
# multiple sequential whitespace into one
def normalize_whitespace(text):
    no_sequential = re.sub(r"[\s]{2,}", " ", text)
    strip = no_sequential.strip()
    return strip

def contraction(match):
    # when called, will find the expanded contraction from the contractions dictionary and return the expanded contraction
    contdict = contractions.contractions
    if contdict.get(match.group()):
        return contdict[match.group()]
    else:
        return match.group()

def expand_contractions(text):
    # look for items 
    replacementPattern = re.compile(r"[a-z]*'[a-z]*")
    another = replacementPattern.sub(contraction, text)
    return another


def clean(text):
    # convert_unicode(text)
    # remove_links(text)
    # remove_emails(text)
    # remove_digits(text)
    lowered = convert_lowercase(text)
    expanded = expand_contractions(lowered)
    no_punc = remove_punctuation(expanded)
    whited = normalize_whitespace(no_punc)
    return whited

# takes a string and divides all the words by whitespace and outputs a list
def tokenize(string):
    tokenizer = WhitespaceTokenizer()
    returnlist = tokenizer.tokenize(string)
    return returnlist

def getwords(doc):
    """ Normalizes and tokenizes the document. Returns a dictionary of the unique words"""

    normalized = clean(doc)
    tokenized = tokenize(normalized)
    # Things to consider:
    # Accuracy is 59.8% when stopwords are removed (compare to 59.1%)
    # However, the classifier predicts "I'm not happy" as positive with
    # stopwords removed
    # and "negative" when they are left in. 
    words = remove_stopwords(tokenized)
    # Return the unique set of words only
    return dict([(w,1) for w in words])
    

if __name__ == '__main__':
    pass