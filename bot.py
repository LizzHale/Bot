class bot:
    def __init__(self, nickname, identity, realname, channel, classifier):
        self.nickname = nickname
        self.identity = identity
        self.realname = realname
        self.channel = channel
        self.classifier = classifier

    def receive_send(self, msg):
        """ When a message is passed to the bot from the socket, 
        sort the messages and pass them to the appropriate 
        method """
        # TO DO - Perhaps these if statements should be in a dictionary organized by conditions/keys methods/values
        if msg[1]=="PRIVMSG" and msg[2]==self.channel:
            return self.classification(" ".join(msg[3:]))

        elif msg[1]=="PRIVMSG" and msg[2]==self.nickname:
            senderNick = msg[0].split("!", 1)[0].strip(":")
            return self.private_message(" ".join(msg[3:]), senderNick)

        elif msg[0]=="PING":
            return self.pong(msg)
            
        elif msg[1]=="JOIN" and msg[2]==self.channel:
            joinerNick = msg[0].split("!", 1)[0].strip(":")
            if not joinerNick == self.nickname:
                reply = "Hello, %s! Seen any good movies lately?" % joinerNick
                return "PRIVMSG %s :%s\r\n" % (self.channel, reply)

        else:
            return False

    def classification(self, msg):
        polarity = self.classifier.classify(msg, default="neutral")
        # TO DO - check how many features and if there are
        # less than two features say: "Tell me more."
        # TO DO - create multiple replies for positive and negative that the 
        # bot can choose at random. 
        if polarity == "positive":
            reply = "Your message was positive"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)

        elif polarity == "negative":
            reply = "Your message was negative"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)
        # TO DO - Use this to continue to train the bot: 
        elif polarity == "neutral":
            reply = "Is that a bad thing or a good thing?"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)
            

    def pong(self, msg):
        return "PONG %s\r\n" % msg[1]

    def private_message(self, msg, sender):
        reply = "Why are we talking in here?"
        return "PRIVMSG %s :%s\r\n" % (sender, reply)
