import math

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func

import config
import normalize
from tables import featurecount, session, categorycount

def getwords(doc):
    """ Normalizes and tokenizes the document. Returns a dictionary of the unique words"""
    normalized = normalize.clean(doc)
    words = normalize.tokenize(normalized)
    # Things to consider:
    # Accuracy is 59.8% when stopwords are removed (compare to 59.1%)
    # However, the classifier predicts "I'm not happy" as positive with
    # stopwords removed
    # and "negative" when they are left in. 
    # words = normalize.remove_stopwords(tokenized)
    # Return the unique set of words only
    return dict([(w,1) for w in words])
    

class classifier:
    def __init__(self, getfeatures,filename=None):

        self.thresholds={}
        # This is the function used to clean and tokenize the data. 
        # getfeatures will return a dictionary of the unique set of words
        self.getfeatures=getfeatures
        # For the fisher classifier
        self.minimums={}
        # The following lines are no longer needed with a database. 
        # # Counts the feature/category combinations
        # self.fc={}
        # # Counts the documents in each category
        # self.cc={}

    def incf(self,f,cat):
        """ Increase the count of the feature/category pair """
        # If the query returns nothing, it will be an empty list (falsey)
        fc = session.query(featurecount).filter_by(feature=f, category=cat).all()
        if fc:
            fc[0].count += 1
        else:
            # If fc is false, create a new instance in the database for the feature and category
            new = featurecount(feature=f, category=cat, count=1)
            session.add(new)

    def incc(self,cat):
        """ Increases the count of the category """

        cc = session.query(categorycount).filter_by(category=cat).all()
        if cc:
            cc[0].count += 1
        else:
            new = categorycount(category=cat, count=1)
            session.add(new)

    def fcount(self,f,cat):
        """ Returns the number of times a feature has appeared in a category """

        feature = session.query(featurecount).filter_by(feature=f, category=cat).all()
        if feature:
            return feature[0].count
        else:
            return 0
    
    def catcount(self,cat):
        """ Returns the total number of items in a category """

        category = session.query(categorycount).filter_by(category=cat).all()
        if category:
            return category[0].count
        else:
            return 0

    def totalcount(self):
        """ Returns the total number of items in all categories """
        # returns a tuple. (4859.0,) Why?
        total = session.query(func.sum(categorycount.count)).one()
        if total:
            return total[0]
        else:
            return 0


    def categories(self):
        """ Returns the list of all the categories """

        category_list = []
        table = session.query(categorycount).all()
        for each in table:
            category_list.append(str(each.category))
        return category_list

    # Takes a document and a category. It uses the 
    # getfeatures method to break the item into its separate features
    # Then calls incf to increase the counts for this category. for every feature
    # finally, it increase the total count for the category.
    def train(self,item,cat):
        """ For the given item/document, the method calls the getfeatures
        function to return the features. Then calls incf method to increase the counts
        for the given category. Lastly, for every feature it increases the total count 
        for the category. """

        features = self.getfeatures(item)

        for f in features:
            self.incf(f,cat)

        self.incc(cat)


    def sampletrain(self):  
        """ For testing purposes, a training sample """

        self.train('Nobody owns the water.', 'good')
        self.train('the quick rabbit jumps fences', 'good')
        self.train('buy pharmaceuticals now', 'bad')
        self.train('make quick money at the online casino', 'bad')
        self.train('the quick brown fox jumps', 'good')
    
    def fprob(self,f,cat):
        """ Returns the probability that a feature is in a category """

        if self.catcount(cat)==0: 
            return 0
        # The total number of times this feature appeared in this
        # category divided by the total number of items in this category
        return self.fcount(f, cat)/self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
        # Calculate current probability
        basicprob=prf(f, cat)
        # Count the number of times this feature has appeared in 
        # all categories
        totals = sum([self.fcount(f, c) for c in self.categories()])
        # Calculate the weight average
        bp = ((weight * ap) + (totals * basicprob))/(weight + totals)
        return bp

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t

    def getthreshold(self,cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    def classify(self,item,default=None):
        """ Returns the probable category for a given item/feature """
        print "This is the classify in the the classifier class"
        probs={}
        # Find the category with the highest probability
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat

        # Make sure the probability exceeds threshold * next best
        for cat in probs:
            if cat==best:
                continue
            if probs[cat]*self.getthreshold(best)>probs[best]: 
                return default
            return best

    def classify_many(self, featuresets): # featuresets must be a list
        """ Gives the option to classify multiple items/documents """

        return [self.classify(fs) for fs in featuresets]

    def accuracy(self, featuresets):
        """ Provides the accuracy rate given a testing_set """

        results = self.classify_many([fs for (fs,l) in featuresets])
        correct = [l==r for ((fs,l), r) in zip(featuresets, results)]
        if correct:
            return float(sum(correct))/len(correct)
        else:
            return 0

class naivebayes(classifier):
    def docprob(self, item, cat):
        """ Multiply the probabilities of all the features together to give the
        probability the document is in the given category """

        features=self.getfeatures(item)
        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):

        catprob = self.catcount(cat)/self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob

### TO DO - Have two bots up and running one with the Bayes and the other with the Pearsons
### In order to continue to train, a certain number of people will need to agree that Bob was mistaken
### Ronald (Fisher) and Thomas (Bayes)
class fisherclassifier(classifier):
    def cprob(self, f, cat):
        # The frequency of this feature in this category
        clf = self.fprob(f, cat)
        if clf == 0: 
            return 0

        # The frequency of this feature in all the categories
        freqsum = sum([self.fprob(f, c) for c in self.categories()])

        # The probability is the frequency in this category divide by the overall frequency
        p = clf/(freqsum)

        return p

    def invchi2(self, chi, df):
        m = chi / 2.0
        s = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            s += term
        return min(s, 1.0)


    def fisherprob(self, item, cat):
        # Multiply all the probabilities together
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))

        # Take the natural log and multiply by -2
        fscore = (-2)*math.log(p)

        # Use the invese chi2 function to get a probability
        return self.invchi2(fscore, len(features)*2)

    def setminimums(self, cat, minim):
        self.minimums[cat] = minim

    def getminimums(self, cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]

    def classify(self, item, default=None):
        # Loop through looking for the best result
        print "This is the classify in the fisher classifier"
        best = default
        maxim = 0.0
        for c in self.categories():
            p = self.fisherprob(item, c)
            print c, p
            # Make sure it exceeds its minimum
            if p > self.getminimums(c) and p > maxim:
                best = c
                maxim = p
        return best

 # Still has problems with Despite the rave reviews, the restaurant did not live up to its potential






