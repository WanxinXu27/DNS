#!/usr/bin/python

from socket import *


def ReceiveQuery():
    serverPort = 53
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('',serverPort))
    print( "The server is ready to receive")
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = SendQueryToResolver(message)
        serverSocket.sendto(modifiedMessage, clientAddress)
        print 'UDP response sent.'


def SendQueryToResolver(message):
    serverName = "8.8.8.8"
    serverPort = 53
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message, (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    clientSocket.close()
    return modifiedMessage


if __name__ == "__main__":
    ReceiveQuery()
