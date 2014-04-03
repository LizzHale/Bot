import unittest

import bot

class TestBotFunctions(unittest.TestCase):

    def testPong(self):
        incoming = "PING :verne.freenode.net"
    
    def testReceiveSend(self):
        incoming = ":orwell.freenode.net NOTICE * :*** Looking up your hostname..."
        incoming2 = ":Noodle!32b82abc@gateway/web/cgi-irc/kiwiirc.com/ip.50.184.42.188 JOIN ##hbtestbot"
        incoming3 = ":Noodle!32b82abc@gateway/web/cgi-irc/kiwiirc.com/ip.50.184.42.188 PRIVMSG ##hbtestbot :what's up"
        incoming4 = ":Noodle!32b82abc@gateway/web/cgi-irc/kiwiirc.com/ip.50.184.42.188 PRIVMSG Bobnut :what's up"



if __name__ == '__main__':
    unittest.main()
 