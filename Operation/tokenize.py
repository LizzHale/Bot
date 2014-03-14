#!/usr/bin/python
from nltk.tokenize import WhitespaceTokenizer

import normalize

#create a list of cleaned for both neg and pos 
def list(pol):
    alist = []

    with open("../Datasets/%s.txt" % pol) as file:
        for line in file:
            data = normalize.clean(line)
            data = tokenize(data)
            alist.append(data)
    return alist

def tokenize(string):
    tokenizer = WhitespaceTokenizer()
    string = tokenizer.tokenize(string)
    return string




