#!/usr/bin/python

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
            positive = normalize.tokenize(positive)
            alist.append((positive, "positive"))

    return alist





