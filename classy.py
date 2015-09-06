import math

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func

import config
from tables import FeatureCount, session, CategoryCount


class Classifier(object):
    def __init__(self, get_features,filename=None):

        self.thresholds={}
        # This is the function used to clean and tokenize the data. 
        # get_features will return a dictionary of the unique set of words
        self.get_features=get_features
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
        fc = session.query(FeatureCount).filter_by(feature=f, category=cat).all()
        if fc:
            fc[0].count += 1
        else:
            # If fc is false, create a new instance in the database for the feature and category
            new = FeatureCount(feature=f, category=cat, count=1)
            session.add(new)

    def incc(self,cat):
        """ Increases the count of the category """

        cc = session.query(CategoryCount).filter_by(category=cat).all()
        if cc:
            cc[0].count += 1
        else:
            new = CategoryCount(category=cat, count=1)
            session.add(new)

    def fcount(self,f,cat):
        """ Returns the number of times a feature has appeared in a category """

        feature = session.query(FeatureCount).filter_by(feature=f, category=cat).all()
        if feature:
            return feature[0].count
        else:
            return 0
    
    def cat_count(self,cat):
        """ Returns the total number of items in a category """

        try:
            category = session.query(CategoryCount).filter_by(category=cat).one()
            return category.count
        except:
            return 0
        # category = session.query(categorycount).filter_by(category=cat).all()
        # if category:
        #     return category[0].count
        # else:
        #     return 0

    def total_count(self):
        """ Returns the total number of items in all categories """
        # returns a tuple. (4859.0,)
        total = session.query(func.sum(CategoryCount.count)).one()
        if total:
            return total[0]
        else:
            return 0


    def categories(self):
        """ Returns the list of all the categories """

        category_list = []
        table = session.query(CategoryCount).all()
        for each in table:
            category_list.append(str(each.category))
        return category_list

    # Takes a document and a category. It uses the 
    # get_features method to break the item into its separate features
    # Then calls incf to increase the counts for this category. for every feature
    # finally, it increase the total count for the category.
    def train(self,item,cat):
        """ For the given item/document, the method calls the get_features
        function to return the features. Then calls incf method to increase the counts
        for the given category. Lastly, for every feature it increases the total count 
        for the category. """

        features = self.get_features(item)

        for f in features:
            self.incf(f,cat)

        self.incc(cat)


    def sample_train(self):  
        """ For testing purposes, a training sample """

        self.train('Nobody owns the water.', 'good')
        self.train('the quick rabbit jumps fences', 'good')
        self.train('buy pharmaceuticals now', 'bad')
        self.train('make quick money at the online casino', 'bad')
        self.train('the quick brown fox jumps', 'good')
    
    def fprob(self,f,cat):
        """ Returns the probability that a feature is in a category """

        if self.cat_count(cat)==0: 
            return 0
        # The total number of times this feature appeared in this
        # category divided by the total number of items in this category
        return self.fcount(f, cat)/self.cat_count(cat)

    def weighted_prob(self, f, cat, prf, weight=1.0, ap=0.5):
        # Calculate current probability
        basicprob=prf(f, cat)
        # Count the number of times this feature has appeared in 
        # all categories
        totals = sum([self.fcount(f, c) for c in self.categories()])
        # Calculate the weight average
        bp = ((weight * ap) + (totals * basicprob))/(weight + totals)
        return bp

    def set_threshold(self,cat,t):
        self.thresholds[cat]=t

    def get_threshold(self,cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    def classify(self,item,default=None):
        """ Returns the probable category for a given item/feature """

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
            if cat == best:
                continue
            if probs[cat]*self.get_threshold(best)>probs[best]: 
                return default
            return best

    def classify_many(self, featuresets): # featuresets must be a list
        """ Gives the option to classify multiple items/documents """

        return [self.classify(fs) for fs in featuresets]

    def accuracy(self, featuresets):
        """ Provides the accuracy rate given a testing_set """

        results = self.classify_many([fs for (fs,l) in featuresets])
        # zip function creates a tuple from two lists
        correct = [l==r for ((fs,l), r) in zip(featuresets, results)]
        if correct:
            return float(sum(correct))/len(correct)
        else:
            return 0

class NaiveBayes(Classifier):
    def doc_prob(self, item, cat):
        """ Multiply the probabilities of all the features together to give the
        probability the document is in the given category """

        features=self.get_features(item)
        p = 1
        for f in features:
            p *= self.weighted_prob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        """ multiplies the category probability by the document probability """
        # category probability is the total number of features in the category divided by the total number of features in the classifier
        catprob = self.cat_count(cat)/self.total_count()

        docprob = self.doc_prob(item, cat)
        return docprob * catprob

class FisherClassifier(Classifier):
    def cprob(self, f, cat):
        """ Divide the frequency in this category by the overall frequency to return the probability """
        # The frequency of this feature in this category
        clf = self.fprob(f, cat)
        if clf == 0: 
            return 0

        # The frequency of this feature in all the categories
        freqsum = sum([self.fprob(f, c) for c in self.categories()])

        # The probability is the frequency in this category divided by the overall frequency
        p = clf/(freqsum)

        return p

    def invchi2(self, chi, df):
        """ Checks if the calculation fits a chi-squared distribution """
        # divide the fisher score by 2.0
        m = chi / 2.0
        # math.exp(-m) is e(approx. 2.718281828) ** -m
        s = math.exp(-m)
        term = math.exp(-m)
        # Remember that df is the len(features)*2 and // returns the floored quotient
        for i in range(1, df//2):
            term *= m / i
            s += term
        # return which ever is smaller - s or 1.0
        return min(s, 1.0)


    def fisher_prob(self, item, cat):
        """ Multiplies all the feature probabilities together. Takes the natural log of this result and then multiplies that by -2. 
        This is then fed through the inverse chi-square function to return the probability that the item is not random"""
        # Multiply all the probabilities together
        p = 1
        features = self.get_features(item)
        for f in features:
            p *= (self.weighted_prob(f, cat, self.cprob))

        # Take the natural log and multiply by -2
        fscore = (-2)*math.log(p)

        # Use the inverse chi-square function to get a probability
        return self.invchi2(fscore, len(features)*2)

    def set_minimums(self, cat, minim):
        self.minimums[cat] = minim

    def get_minimums(self, cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]

    def classify(self, item, default=None):
        # Loop through looking for the best result
        best = default
        maxim = 0.0
        for c in self.categories():
            p = self.fisher_prob(item, c)
            # Make sure it exceeds its minimum
            if p > self.get_minimums(c) and p > maxim:
                best = c
                maxim = p
        return best








