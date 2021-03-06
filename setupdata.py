import classy
import config
import normalize
from tables import session

def get_list(polarity):
    """ From the stored data, creates a tuple with the data string and category """

    polarityList = []
    with open("Datasets/%s.txt" % polarity[:3]) as data:
        for line in data:
            tupledPolarity = (line, polarity)
            polarityList.append(tupledPolarity)       
    return polarityList

def get_training_set():
    """ Uses 75% of the positive and negative data for training the classifier """

    negative = get_list("negative")
    positive = get_list("positive")
    training_set = negative[:int(len(negative)*.75)] + positive[:int(len(positive)*.75)]
    return training_set

def get_test_set():
    """ Uses 25% of the positive and negative data for testing the classifier """

    negative = get_list("negative")
    positive = get_list("positive")
    test_set = negative[int(len(negative)*.75):] + positive[int(len(positive)*.75):]
    return test_set

def train(classifier, training_set, database):   
    """ For the given classifier and training data, trains the classifier and commits to the database """

    for each in training_set:
        classifier.train(each[0], each[1])   
     
    session.commit()

def test(classifier, test_set):
    """ Calls the accuracy method on the test data for the given classifier """
    # accuracy with the naivebayes classifier is at 59.8% 
    # accuracy with the fisher classifier is at 64.39%
    return classifier.accuracy(test_set)

def getclassifier():
    """ Creates an instance of the classifier """
    # TO DO - set a minimum for both categories. Perhaps lower than 60% for both will return "neutral"
    classifier = classy.FisherClassifier(normalize.get_words)
    classifier.set_minimums("positive", .60)
    classifier.set_minimums("negative", .60)
    return classifier

def stats(msg):
    """ Returns a dictionary with the classification information for the received message for use in the browser """

    ronald = getclassifier()
    statsDict = {"features": {}, "message": msg, }


    features = ronald.get_features(msg)

    for key in features:
        negkeyprob = round((ronald.cprob(key, "negative")*100), 3)
        poskeyprob = round((ronald.cprob(key, "positive")*100), 3)
        statsDict["features"][key] = {"negative": negkeyprob, "positive": poskeyprob}

    negmsgprob = round((ronald.fisher_prob(msg, "negative")*100), 2)
    posmsgprob = round((ronald.fisher_prob(msg, "positive")*100), 2)


    statsDict["docprob"] = {"negative": negmsgprob, "positive": posmsgprob}

    statsDict["classification"] = ronald.classify(msg)

    return statsDict

def comparison(msg):
    """ Returns a dictionary with the classifications a the received message from both of the classifiers for comparison """
    
    ronald = classy.FisherClassifier(normalize.get_words)
    thomas = classy.NaiveBayes(normalize.get_words)
    featureDict = ronald.get_features(msg)

    comparisonDict = {"message": msg}

    features = []
    for key in featureDict:
        features.append(key)

    comparisonDict["features"] = features

    comparisonDict["Ronald"] = ronald.classify(msg)
    comparisonDict["Thomas"] = thomas.classify(msg)

    return comparisonDict


if __name__ == "__main__":
    cl = getclassifier()
    training = get_training_set()
    train(cl, training, config.DB_URL)
