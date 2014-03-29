import unittest

import normalize

class TestNormalizeFunctions(unittest.TestCase):

    def test_lower(self):
        text = "The quick BROWN fox jumps over the lazY Dog"

        t = normalize.convert_lowercase(text)

        self.assertEqual(t, 'the quick red fox jumps over the lazy dog')

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