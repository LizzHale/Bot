class bot:
    def __init__(self, host, port, nickname, identity, realname, channel):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.identity = identity
        self.realname = realname
        self.channel = channel

    def connect(socket):
        socket.connect((self.host, self.port))

    def nickname(socket):
        socket.send("NICK %s\r\n" % self.nickname)

    def user(socket):
        socket.send("USER %s %s bla :%s\r\n" % (self.identity, self.host, self.realname))

    def join(socket):
        socket.send("JOIN %s\r\n" % self.channel)

    def receive():
        pass

    def send():
        pass