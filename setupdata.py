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
    # accuracy with the fisher classifier is at ?
    return classifier.accuracy(test_set)

def getclassifier():
    """ Creates an instance of the classifier """
    # TO DO - create two different functions for the two different classifiers
    classifier = classy.naivebayes(classy.getwords)
    return classifier

if __name__ == "__main__":
    cl = getclassifier()
    training = get_training_set()
    train(cl, training, config.DB_URL)
