import re
import unittest


import normalize

class TestNormalizeFunctions(unittest.TestCase):

    def testLower(self):
        text = "The quick BROWN fox jumps over the lazY Dog"

        t = normalize.convert_lowercase(text)

        self.assertNotEqual(t, 'the quick red fox jumps over the lazy dog')
        self.assertEqual(t, 'the quick brown fox jumps over the lazy dog')

    def testRemoveLinks(self):
        text = "visit us at www.we.com"
        text2 = "visit us at we.com"
        text3 = "visit us at we.edu"

        t = normalize.remove_links(text)

        self.assertEqual(t, "visit us at ")

        t = normalize.remove_links(text2)

        self.assertEqual(t, "visit us at ")

        t = normalize.remove_links(text3)

        self.assertEqual(t, "visit us at ")

    def testRemoveEmails(self):
        text = "you can email me at lizzhale@mac.com"

        t = normalize.remove_emails(text)

        self.assertEqual(t, "you can email me at ")

    def testRemoveDigits(self):
        text = "It was rated 101 out of 3000 movies."

        t = normalize.remove_digits(text)

        self.assertNotIn("101", t)
        self.assertNotIn("3000", t)
        self.assertEqual(t, "It was rated     out of      movies.")

    def testRemoveStopwords(self):
        testList = ["those", "golden", "hills", "are", "further", "than", "you", "think"]
        
        l = normalize.remove_stopwords(testList)

        self.assertNotIn("those", l)
        self.assertNotIn("are", l)
        self.assertNotIn("further", l)
        self.assertNotIn("than", l)
        self.assertNotIn("you", l)

    def testRemovePunctuation(self):
        text = "What? I can't believe it! In this day in age, it's f*#&ing unacceptable"

        t = normalize.remove_punctuation(text)

        self.assertEqual(t, "What  I can t believe it  In this day in age  it s f   ing unacceptable")

    def testNormalizeWhitespace(self):
        text = "What  I can t believe it  In this day in age  it s f   ing unacceptable "

        t = normalize.normalize_whitespace(text)

        self.assertEqual(t, "What I can t believe it In this day in age it s f ing unacceptable")

    def testContraction(self):
        text = "i'll"
        text2 = "the book's"

        replacementPattern = re.compile(r"[a-z]*'[a-z]*")
        r = replacementPattern.sub(normalize.contraction, text)

        self.assertEqual(r, "i will") 

        replacementPattern = re.compile(r"[a-z]*'[a-z]*")
        r = replacementPattern.sub(normalize.contraction, text2)

        self.assertEqual(r, "the book's" )

    def testExpandContractions(self):
        text = "i'll"
        text2 = "i'll've"
        text3 = "He's"
        text4 = "ne'er"

        t = normalize.expand_contractions(text)

        self.assertEqual(t, "i will")

        t = normalize.expand_contractions(text2)

        self.assertEqual(t, "i will have")

        t = normalize.expand_contractions(text3)

        self.assertNotEqual(t, "He is")

        t = normalize.expand_contractions(text4)

        self.assertEqual(t, "never")



    def testClean(self):
        text = "an unsatisfying ending to what is ultimately one of the immensely talented Mr McEwan's decidedly lesser efforts."
        text4 = "Fare thee well, for ne'er shall I return."
        text2 = "DO remember to contact me at Lizzhale@mac.com"
        text3 = "It was rated 101 out of 3000 movies."

        t = normalize.clean(text)

        self.assertIs(type(t), str)
        self.assertEqual(t, "an unsatisfying ending to what is ultimately one of the immensely talented mr mcewan s decidedly lesser efforts")
        
        t = normalize.clean(text4)

        self.assertEqual(t, "fare thee well for never shall i return")

        t = normalize.clean(text2)

        self.assertEqual(t, "do remember to contact me at")

        t = normalize.clean(text3)

        self.assertEqual(t, "it was rated out of movies")

    def testTokenize(self):
        text = "fare thee well for never shall i return"

        l = normalize.tokenize(text)

        self.assertIs(type(l), list)
        self.assertEqual(l, ["fare", "thee", "well", "for", "never", "shall", "i", "return"])

    def testGetWords(self):
        text = 'Although Mr. DeLillo extracts considerable suspense from his story, while building a Pinteresque sense of dread, there is something suffocating and airless about this entire production. '

        d = normalize.getwords(text)

        self.assertIs(type(d), dict)
        self.assertDictEqual({'building': 1, 'entire': 1, 'story': 1, 'suffocating': 1, 'extracts': 1, 'sense': 1, 'pinteresque': 1, 'production': 1, 'suspense': 1, 'dread': 1, 'although': 1, 'mr': 1, 'airless': 1, 'delillo': 1, 'considerable': 1, 'something': 1}, d)

if __name__ == '__main__':
        unittest.main()
 

# Hook will work because the process will exit with a code and then a shell script will tell it 
# how to behave based on that. 
""" Test driven development for complex features -- 
perhaps use this for the last feature I write
Red, green, refactor - first have a failing test case, then write it to make it green, then refactor
Regression side of testing is to avoid being slowed down by bugs. So test the next thing you are 
going to change.
Tests are often called specs because they are a form of documentation.
In memory databases will allow you test but not "commit" the test processes.
"""