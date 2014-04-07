from normalize import clean

class bot:
    def __init__(self, nickname, identity, realname, channel, classifier):
        self.nickname = nickname
        self.identity = identity
        self.realname = realname
        self.channel = channel
        self.classifier = classifier
        self.joke = 0

    def receive_send(self, msg):
        """ When a message is passed to the bot from the socket, 
        sort the messages and pass them to the appropriate 
        method """
        # TO DO - Perhaps these if statements should be in a dictionary organized by conditions/keys methods/values
        if msg[1]=="PRIVMSG" and msg[2]==self.channel:
            message = (" ").join(msg[3:]).strip(":")
            if clean(message)=="knock knock" or self.joke > 0:
                return self.laugh(message)
            else:
                return self.classification(message)

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

    def laugh(self, msg):
        if clean(msg) == "knock knock":
            self.joke = 1
            reply = "Who's there?"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)
        elif self.joke == 1:
            self.joke = 2
            reply = msg + " who?"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)
        elif self.joke == 2:
            self.joke = 0
            polarity = self.classifier.classify(msg, default="neutral")
            if polarity == "positive":
                reply = "That's hilarious"
                return "PRIVMSG %s :%s\r\n" % (self.channel, reply)
            elif polarity == "negative":
                reply = "That's not very funny."
                return "PRIVMSG %s :%s\r\n" % (self.channel, reply)
            elif polarity == "neutral":
                reply = "I'm not sure what to think about that."
                return "PRIVMSG %s :%s\r\n" % (self.channel, reply)
        else:
            self.joke = 0
            reply = "What were we talking about?"
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)


    def classification(self, msg):
        """ Classify the received message and send back a reply """

        polarity = self.classifier.classify(msg, default="neutral")
        features = self.classifier.getfeatures(msg)
        # Messages with less than 3 features are not as accurate. Get more information for the 
        # chat participant
        if len(features) < 3:
            reply = "Tell me more..."
            return "PRIVMSG %s :%s\r\n" % (self.channel, reply)

        else:
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
