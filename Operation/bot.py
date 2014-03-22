
class bot:
    def __init__(self, nickname, identity, realname, channel, classifier):
        self.nickname = nickname
        self.identity = identity
        self.realname = realname
        self.channel = channel
        self.classifier = classifier

    def receive_send(self, msg):

        if msg[1]=="PRIVMSG" and msg[2]==self.channel:
            return self.classification(msg[3])

        elif msg[0]=="PING":
            return self.pong(msg)
            
        else:
            return False

    def classification(self, msg):
        polarity = self.classifier.classify(msg, default="neutral")
        # TODO - check how many features and if there are
        # less than two features say: "Tell me more."
        if polarity == "positive":
            reply = "Your message was positive"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)

        elif polarity == "negative":
            reply = "Your message was negative"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)

        elif polarity == "neutral":
            reply = "Is that a bad thing or a good thing?"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)
            

    def pong(self, msg):
        return "PONG %s\r\n" % msg[1]

       # # when a message to the channel is received, the bot will say hello
            # # TO DO obviously I don't want it responding "hello" every single time
            # if line[1]=="PRIVMSG" and line[2]==CHANNEL:
            #     # Added quit command to shutdown the bot
            #     if line[3]==":quit":
            #         s.send("QUIT \r\n")
            #     else:
            #         msg = "hello"
            #         s.send("PRIVMSG %s %s\r\n" % (CHANNEL, msg))

            # # Can respond to "private messages" and respond directly back to the speaker
            # if line[1]=="PRIVMSG" and line[2]==NICK:
            #     # line 0 is the originator parameter
            #     # in this next line, we split on ! taking the left half
            #     # and then strip the preceeding colon to get the sender's nickname
            #     senderNick = line[0].split("!", 1)[0].strip(":")
            #     msg = "hello"
            #     s.send("PRIVMSG %s %s\r\n" % (senderNick, msg))