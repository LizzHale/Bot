#!/usr/bin/python

import nltk

import normalize

# returns a list of cleaned and tokenized tuples for both neg and pos 
def list_of_statements():
    alist = []
    stopwords = nltk.corpus.stopwords.words('english')
    with open("../Datasets/neg.txt") as neg:
        for line in neg:
            # makes lowercase, expands contractions, 
            # removes punctuation and normalizes whitespace
            negative = normalize.clean(line)
            negative = normalize.tokenize(negative)
            negative = normalize.remove_stopwords(negative)
            alist.append((negative, "negative"))

    with open("../Datasets/pos.txt") as pos:
        for line in pos:
            positive = normalize.clean(line)
            positive = normalize.tokenize(positive)
            positive = normalize.remove_stopwords(positive)
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

# returns a dictionary (key is contains(the word) and the value is whether or not the word exists in the statement)
def extract_features(statement):
    statement_words = set(statement)
    word_features = get_word_features(get_words_in_corpus(list_of_statements()))
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in statement_words)
    return features

def main():
    train_statements = list_of_statements()
    #test_set = nltk.classify.apply_features(extract_features, test_statements)
    training_set = nltk.classify.apply_features(extract_features, train_statements)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    return classifier

# if __name__ =='__main__':
#     main()






