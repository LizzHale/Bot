import sys
import socket


HOST="irc.freenode.net"
PORT=6667
NICK="Bobnut"
IDENT="bobnut"
REALNAME="Bob DeKokosnoot"
readbuffer=""
CHANNEL="##hbtestbot"
ID="~bobnut@c-50-184-42-188.hsd1.ca.comcast.net"

s=socket.socket()
# The CONNECT command is used to establish a new connection with a server
s.connect((HOST, PORT))
# The NICK command is used to give user a nickname 
s.send("NICK %s\r\n" % NICK)
# The USER command is used at the beginning of a connection
# to specify the username, hostname, and realname of a new user.
# what is bla?
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
# TO DO - add a JOIN command: s.send("JOIN %s\r\n" % CHANNEL) ???
# Should receive back a RPL_TOPIC (channel's topic) and RPL_NAMREPLY (list of users)
s.send("JOIN %s\r\n" % CHANNEL)

while 1:
    # at first, readbuffer is an empty string. Each time through the while loop
    # readbuffer is the last item from the temp list.
    # It is concatenated to the incoming data from the host
    readbuffer = readbuffer+s.recv(1024)
    # string.split - splits readbuffer on each newline and formats in a list
    temp = readbuffer.split("\n")
    # removes the last item on the temp string. Not sure why though.
    readbuffer = temp.pop()


    # loop through the items in the the temp list
    for line in temp:
        print line
        # remove whitespace on the sides
        line = line.strip()
        # split on whitespace - returns a list
        line = line.split()


        # if the server "pings" my bot, it needs to respond with
        # pong and whatever the server ping'd. 
        # this tells the server that I am active so it won't kick me off
        # PING messages look like this: PING :something.freenode.net
        if line[0]=="PING":
            sent = s.send("PONG %s\r\n" % line[1])

        if line[1]=="PRIVMSG" and line[2]==CHANNEL:
            msg = "hello"
            sent = s.send("PRIVMSG %s %s\r\n" % (CHANNEL, msg))

        if line[1]=="PRIVMSG" and line[2]==NICK:
            sentBy = line[0].split("!", 1)
            senderNick = sentBy[0].strip(":")
            print sentBy
            print senderNick
            msg = "hello"
            s.send("PRIVMSG %s %s\r\n" % (senderNick, msg))

# TO DO add a QUIT command
