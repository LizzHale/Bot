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
    pass

def remove_digits(text):
    return ""

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
    print match
    # when called, will find the expanded contraction from the contractions dictionary and return the expanded contraction
    contdict = contractions.contractions
    if contdict.get(match.group()):
        return contdict[match.group()]
    else:
        return match.group()

def expand_contractions(text):
    # look for items 
    replacementPattern = re.compile(r"[a-z]*'[a-z]*")
    print replacementPattern
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


if __name__ == '__main__':
    clean()