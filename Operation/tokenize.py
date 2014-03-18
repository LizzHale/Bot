#!/usr/bin/python
from nltk.tokenize import WhitespaceTokenizer

import normalize

#create a list of cleaned and tokenized tuples for both neg and pos 
def list_of_statements():
    alist = []

    with open("../Datasets/neg.txt") as neg:
        for line in neg:
            # makes lowercase, expands contractions, 
            # removes punctuation and normalizes whitespace
            negative = normalize.clean(line)
            negative = tokenize(negative)
            alist.append((negative, "negative"))

    with open("../Datasets/pos.txt") as pos:
        for line in pos:
            positive = normalize.clean(line)
            positive = tokenize(positive)
            alist.append((positive, "positive"))

    return alist


# takes a string and divides all the words by whitespace and outputs a list
def tokenize(string):
    tokenizer = WhitespaceTokenizer()
    string = tokenizer.tokenize(string)
    return string



