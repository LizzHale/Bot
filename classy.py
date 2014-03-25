from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

import config
import normalize

def getwords(doc):
    normalized = normalize.clean(doc)
    tokenized = normalize.tokenize(normalized)
    # Things to consider:
    # Accuracy is 59.8% when stopwords are removed (compare to 59.1%)
    # However, the classifier predicts "I'm not happy" as positive with
    # stopwords removed
    # and "negative" when they are left in. 
    words = normalize.remove_stopwords(tokenized)
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

    # Opens a database for this classifer and creates tables if necessary
    def setdb(self, database):
        self.engine = create_engine(config.DB_URL, echo=False) 
        self.session = self.engine.scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

        self.Base = declarative_base()
        self.Base.query = session.query_property()
        
    # Increase the count of a feature/category pair
    def incf(self,f,cat):
        count = self.fcount(f, cat)
        if count == 0:
            self.conn.execute("INSERT INTO fc VALUES ('%s', '%s', 1)" % (f, cat))
        else:
            self.conn.execute("UPDATE fc SET count=%d WHERE feature='%s' AND category='%s'" % (count+1, f, cat))

    #Increase the count of a category
    def incc(self,cat):
        count = self.catcount(cat)
        if count == 0:
            self.conn.execute("INSERT INTO cc VALUES ('%s', 1)" % (cat))
        else:
            self.conn.execute("UPDATE cc SET count=%d WHERE category='%s'" % (count+1, cat))

    # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
        res = self.conn.execute("SELECT count FROM fc WHERE feature='%s' AND category='%s'" % (f, cat)).fetchone()
        if res == None:
            return 0
        else:
            return float(res[0])

    # The number of items in a category
    def catcount(self,cat):
        res = self.conn.execute('SELECT count FROM cc WHERE category="%s"' %(cat)).fetchone()
        if res == None:
            return 0
        else:
            return float(res[0])
    # The total number of items
    def totalcount(self):
        res = self.conn.execute('SELECT sum(count) FROM cc').fetchone()
        if res == None:
            return 0
        return res[0]

    # The list of all categories
    def categories(self):
        cur = self.conn.execute('SELECT category FROM cc')
        return [d[0] for d in cur]

    # Takes a document and a classification. It uses the 
    # getfeatures method to break the item into its separate features
    # The calls incf to increase the counts for this classification for every feature
    # finally, it increase the total count for this classification
    def train(self,item,cat):
        features=self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f,cat)
        #Increment the count for this category
        self.incc(cat)
    
    def commit(self):
        self.conn.commit()


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





