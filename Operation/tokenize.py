#!/usr/bin/python
from nltk.tokenize import WhitespaceTokenizer

import normalize

#create a list of cleaned for both neg and pos 
def list(pol):
    alist = []

    with open("../Datasets/%s.txt" % pol) as file:
        for line in file:
            # makes lowercase, expands contractions, 
            # removes punctuation and normalizes whitespace
            data = normalize.clean(line)
            data = tokenize(data)
            alist.append(data)
    return alist

# takes a string and divides all the words by whitespace and outputs a list
def tokenize(string):
    tokenizer = WhitespaceTokenizer()
    string = tokenizer.tokenize(string)
    return string



