#!/usr/bin/python

import nltk

import normalize

# returns a list of cleaned and tokenized tuples for both neg and pos 
def list_of_statements():
    alist = []

    with open("../Datasets/neg.txt") as neg:
        for line in neg:
            # makes lowercase, expands contractions, 
            # removes punctuation and normalizes whitespace
            negative = normalize.clean(line)
            negative = normalize.tokenize(negative)
            alist.append((negative, "negative"))

    with open("../Datasets/pos.txt") as pos:
        for line in pos:
            positive = normalize.clean(line)
            positive = normalize.tokenize(positive)
            alist.append((positive, "positive"))

    return alist

# takes a list of cleaned and tokenized tuples (annotated either positive or negative)
# and returns a list of all the words
def get_words_in_corpus(tupledList):
    all_words = []
    for (words, sentiment) in tupledList:
        all_words.extend(words)
    return all_words

# returns an ordered list (first by frequency then alphabetically) of unique words
def get_word_features(wordList):
    # FreqDist returns a dictionary key - word value - frequency
    wordList = nltk.FreqDist(wordList)
    word_features = wordList.keys()
    return word_features

def main():
    return get_word_features(get_words_in_corpus(list_of_statements()))


if __name__ =='__main__':
    main()






