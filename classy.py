from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func

import config
import normalize
from tables import featurecount, session, categorycount

def getwords(doc):
    normalized = normalize.clean(doc)
    tokenized = normalize.tokenize(normalized)
    # Things to consider:
    # Accuracy is 59.8% when stopwords are removed (compare to 59.1%)
    # However, the classifier predicts "I'm not happy" as positive with
    # stopwords removed
    # and "negative" when they are left in. 
   #words = normalize.remove_stopwords(tokenized)
    # Return the unique set of words only
    return dict([(w,1) for w in words])
    

class classifier:
    def __init__(self, getfeatures,filename=None):
        self.thresholds={}
        # Counts the feature/category combinations
        self.fc={}
        # Counts the documents in each category
        self.cc={}
        # This is the function that cleans the messages and returns 
        # The features
        self.getfeatures=getfeatures

    # Increase the count of a feature/category pair
    def incf(self,f,cat):
        print f 
        print cat
        ## query here, get object
        fc = session.query(featurecount).filter_by(feature=f, category=cat).all()
        # Test if fc will ever be False. The query will return an empty list
        print fc
        if fc:
            fc[0].count += 1
        else:
            #create a new one!
            new = featurecount(feature=f, category=cat, count=1)
            session.add(new)
    #Increase the count of a category
    def incc(self,cat):
        cc = session.query(categorycount).filter_by(category=cat).all()
        if cc:
            cc[0].count += 1
        else:
            new = categorycount(category=cat, count=1)
            session.add(new)
    # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
        feature = session.query(featurecount).filter_by(feature=f, category=cat).all()
        if feature:
            return feature[0].count
        else:
            return 0
    

    # The number of items in a category
    def catcount(self,cat):
        category = session.query(categorycount).filter_by(category=cat).all()
        if category:
            return category[0].count
        else:
            return 0

    # The total number of items
    def totalcount(self):
        # returns a tuple. (4859.0,) Why?
        total = session.query(func.sum(categorycount.count)).one()
        if total:
            return total[0]
        else:
            return 0

    # The list of all categories
    def categories(self):
        category_list = []
        table = session.query(categorycount).all()
        for each in table:
            category_list.append(str(each.category))
        return category_list

    # Takes a document and a classification. It uses the 
    # getfeatures method to break the item into its separate features
    # The calls incf to increase the counts for this classification for every feature
    # finally, it increase the total count for this classification
    def train(self,item,cat):
        features=self.getfeatures(item)
        print features
        # Increment the count for every feature with this category
        for f in features:
            print f 
            print cat
            self.incf(f,cat)
        #Increment the count for this category
        self.incc(cat)


    def sampletrain(cl):
        cl.train('Nobody owns the water.', 'good')
        cl.train('the quick rabbit jumps fences', 'good')
        cl.train('buy pharmaceuticals now', 'bad')
        cl.train('make quick money at the online casino', 'bad')
        cl.train('the quick brown fox jumps', 'good')
    
    # Calculates the probability that a word is in a particular category
    def fprob(self,f,cat):
        if self.catcount(cat)==0: 
            return 0
        # The total number of times this feature appeared in this
        # category divided by the total number of items in this category
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # Calculate current probability
        basicprob=prf(f,cat)
        # Count the number of times this feature has appeared in 
        # all categories
        totals = sum([self.fcount(f,c) for c in self.categories()])
        # Calculate the weight average
        bp = ((weight*ap) + (totals*basicprob))/(weight+totals)
        return bp

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t

    def getthreshold(self,cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    def classify(self,item,default=None):
        probs={}
        # Find the category with the highest probability
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat

        # Make sure the probability exceeds threshold*next best
        for cat in probs:
            if cat==best:
                continue
            if probs[cat]*self.getthreshold(best)>probs[best]: 
                return default
            return best

    def classify_many(self, featuresets):
        return [self.classify(fs) for fs in featuresets]

    def accuracy(self, featuresets):
        results = self.classify_many([fs for (fs,l) in featuresets])
        correct = [l==r for ((fs,l), r) in zip(featuresets, results)]
        if correct:
            return float(sum(correct))/len(correct)
        else:
            return 0

class naivebayes(classifier):
    def docprob(self, item, cat):
        features=self.getfeatures(item)

        # multiply the probabilities of all the features together
        p=1
        for f in features:
            p*=self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item, cat)
        return docprob*catprob






