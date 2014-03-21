#!/usr/bin/python

import socket
import sys


HOST="irc.freenode.net"
PORT=6667
NICK="Bobnut"
IDENT="bobnut"
REALNAME="Bob DeKokosnoot"
CHANNEL="##hbtestbot"

def bot_socket():
    # readbuffer is needed because you might not be able to read complete IRC commands
    # from the server. 
    readbuffer=""
    s=socket.socket()
    # The CONNECT command is used to establish a new connection with a server
    s.connect((HOST, PORT))
    # The NICK command is used to give user a nickname 
    s.send("NICK %s\r\n" % NICK)
    # The USER command is used at the beginning of a connection
    # to specify the username, hostname, and realname of a new user.
    # Turns out that bla is needed for registration 
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    # TO DO - add a JOIN command: s.send("JOIN %s\r\n" % CHANNEL) ???
    # Should receive back a RPL_TOPIC (channel's topic) and RPL_NAMREPLY (list of users)
    s.send("JOIN %s\r\n" % CHANNEL)

    while 1:
        # at first, readbuffer is an empty string. Each time through the while loop
        # readbuffer is the last item from the temp list.
        # It is concatenated to the incoming data from the host
        # why 1024?
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
                print "PONG %s\r\n" % line[1]
                # FYI send returns the number of bytes sent.
                sent = s.send("PONG %s\r\n" % line[1])

            # when a message to the channel is received, the bot will say hello
            # TO DO obviously I don't want it responding "hello" every single time
            if line[1]=="PRIVMSG" and line[2]==CHANNEL:
                # Added quit command to shutdown the bot
                if line[3]==":quit":
                    s.send("QUIT \r\n")
                else:
                    msg = "hello"
                    s.send("PRIVMSG %s %s\r\n" % (CHANNEL, msg))

            # Can respond to "private messages" and respond directly back to the speaker
            if line[1]=="PRIVMSG" and line[2]==NICK:
                # line 0 is the originator parameter
                # in this next line, we split on ! taking the left half
                # and then strip the preceeding colon to get the sender's nickname
                senderNick = line[0].split("!", 1)[0].strip(":")
                msg = "hello"
                s.send("PRIVMSG %s %s\r\n" % (senderNick, msg))

if __name__ == '__main__':
    bot_socket()
