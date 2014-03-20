import docclass
import normalize

def getlist(polarity):
    polarityList = []
    with open("../Datasets/%s.txt" % polarity[:3]) as data:
        for line in data:
            tupledPolarity = (line, polarity)
            polarityList.append(tupledPolarity)       
    return polarityList

def train():
    negative = getlist("negative")
    positive = getlist("positive")
    training_data = negative[:len(negative)/2]
    training_data.extend(positive[:len(positive)/2])
    cl = docclass.naivebayes(docclass.getwords)
    for each in training_data:
        cl.train(each[0], each[1])
    return cl

def accuracy(classifier, gold):
    results = classifier.classify_many([fs for (fs,l) in gold])
    correct = [l==r for ((fs,l), r) in zip(gold, results)]
    if correct:
        return float(sum(correct))/len(correct)
    else:
        return 0

def test():
    cl = train()
    negative = getlist("negative")
    positive = getlist("positive")
    testing_data = negative[len(negative)/2:]
    testing_data.extend(positive[len(positive)/2:])
    return accuracy(cl, testing_data)

