#!/usr/bin/python

import socket
import sys
import os

import bot
import setupdata
from tables import session


HOST=os.environ.get("HOST")
BOT_PORT=int(os.environ.get("BOT_PORT"))
NICK=os.environ.get("NICK")
IDENT=os.environ.get("IDENT")
REALNAME=os.environ.get("REALNAME")
CHANNEL=os.environ.get("CHANNEL")


# the classifier is currently a fisherclassifier 3/29
CLASSIFIER=setupdata.getclassifier()

def bot_socket():
    # readbuffer is needed because you might not be able to read complete IRC commands
    # from the server. 
    readbuffer=""

    # Instantiate the bot
    bob = bot.Bot(NICK, IDENT, REALNAME, CHANNEL, CLASSIFIER)

    s=socket.socket()

    # The CONNECT command is used to establish a new connection with a server
    s.connect((HOST, BOT_PORT))
    # The NICK command is used to give user a nickname 
    s.send("NICK %s\r\n" % bob.nickname)
    # The USER command is used at the beginning of a connection
    # to specify the username, hostname, and realname of a new user.
    # Turns out that bla is needed for registration 
    s.send("USER %s %s bla :%s\r\n" % (bob.identity, HOST, bob.realname))
    # TO DO - add a JOIN command: s.send("JOIN %s\r\n" % CHANNEL) ???
    # Should receive back a RPL_TOPIC (channel's topic) and RPL_NAMREPLY (list of users)
    s.send("JOIN %s\r\n" % bob.channel)

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
            # send all messages to the bot to process
            reply = bob.receive_send(line)
            if reply:
                s.send(reply)
            
            


if __name__ == '__main__':
    bot_socket()
