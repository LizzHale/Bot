
class bot:
    def __init__(self, nickname, identity, realname, channel, classifier):
        self.nickname = nickname
        self.identity = identity
        self.realname = realname
        self.channel = channel
        self.classifier = classifier

    def receive_send(self, msg):

        if msg[1]=="PRIVMSG" and msg[2]==self.channel:
            return self.classification(" ".join(msg[3:]))

        elif msg[1]=="PRIVMSG" and msg[2]==self.nickname:
            senderNick = msg[0].split("!", 1)[0].strip(":")
            return self.private_message(" ".join(msg[3:]), senderNick)

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

    def private_message(self, msg, sender):
        reply = "Why are we talking in here?"
        return "PRIVMSG %s :%s\r\n" % (sender, reply)
