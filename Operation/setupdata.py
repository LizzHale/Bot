import classy
import normalize

def get_list(polarity):
    polarityList = []
    with open("../Datasets/%s.txt" % polarity[:3]) as data:
        for line in data:
            tupledPolarity = (line, polarity)
            polarityList.append(tupledPolarity)       
    return polarityList

def get_training_set():
    negative = get_list("negative")
    positive = get_list("positive")
    training_set = negative[:int(len(negative)*.75)] + positive[:int(len(positive)*.75)]
    return training_set

def get_test_set():
    negative = get_list("negative")
    positive = get_list("positive")
    test_set = negative[int(len(negative)*.75):] + positive[int(len(positive)*.75):]
    return test_set

def train(training_set):
    classifier = classy.naivebayes(classy.getwords)
    # it's possible to set the threshold but experiments show that a threshold of 2 produces 20% accuracy
    for each in training_set:
        classifier.train(each[0], each[1])
    return classifier

def test(classifier, test_set):
    return classifier.accuracy(test_set)
