import unittest

import bot
import setupdata

class TestBotFunctions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBotFunctions, self).__init__(*args, **kwargs)
        self.classifier = setupdata.getclassifier()
        self.bot = bot.bot("TestBob", "TestBob", "Bob's Doppleganger", "##hbtestbot", self.classifier)


    def testPong(self):
        incoming = ["PING", ":verne.freenode.net"]

        out = self.bot.pong(incoming)

        self.assertEqual(out, "PONG :verne.freenode.net\r\n")
    
    def testReceiveSend(self):
        incoming = [":orwell.freenode.net", "NOTICE", "*", ":***", "Looking up your hostname..."]

        out = self.bot.receive_send(incoming)

        self.assertFalse(out)

        incoming2 = [":Noodle!32b82abc@gateway/web/cgi-irc/kiwiirc.com/ip.50.184.42.188", "JOIN", "##hbtestbot"]
        
        out = self.bot.receive_send(incoming2)

        self.assertTrue(out)

        incoming3 = [":Noodle!32b82abc@gateway/web/cgi-irc/kiwiirc.com/ip.50.184.42.188", "PRIVMSG", "##hbtestbot", ":what's up"]
        
        out = self.bot.receive_send(incoming3)

        self.assertTrue(out)

        incoming4 = [":Noodle!32b82abc@gateway/web/cgi-irc/kiwiirc.com/ip.50.184.42.188", "PRIVMSG", "TestBob", ":what's up"]

        out = self.bot.receive_send(incoming4)

        self.assertTrue(out)

    def testClassification(self):
        incoming = "what's up"
        
        out = self.bot.classification(incoming)

        self.assertIsNotNone(out)

if __name__ == '__main__':
    unittest.main()
 