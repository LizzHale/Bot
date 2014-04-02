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

        t = normalize.remove_links(text)

        self.assertEqual(t, "you can email me at ")

    def testRemoveDigits(self):
        text = "It was rated 101 out of 3000 movies."

        t = normalize.remove_digits(text)

        self.assertNotIn("101", t)
        self.assertNotIn("3000", t)
        self.assertEqual(t, "It was rated out of movies")

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
        # Test a contraction like i'll've and ne'er
        pass

    def testClean(self):
        text = "Fare thee well, for ne'er shall I return."
        text2 = "DO remember to contact me at Lizzhale@mac.com"
        text3 = "It was rated 101 out of 3000 movies."

        t = normalize.clean(text)

        self.assertEqual(t, "fare thee well for never shall i return")
        self.assertEqual(t, "do remember to contact me at")
        self.assertEqual(t, "it was rated out of movies")

    def testTokenize(self):
        text = "fare thee well for never shall i return"

        l = normalize.tokenize(text)

        self.assertEqual(l, ["fare", "thee", "well", "for", "never", "shall", "i", "return"])


if __name__ == '__main__':
    try: 
        unittest.main()
    except:
        pass

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