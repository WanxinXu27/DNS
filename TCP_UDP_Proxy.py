#!/usr/bin/python

from socket import *


def ReceiveQuery():
    serverPort_UDP = 53
    serverSocket_UDP = socket(AF_INET, SOCK_DGRAM)
    serverSocket_UDP.bind(('', serverPort_UDP))

    serverPort_TCP = 53
    serverSocket_TCP = socket(AF_INET, SOCK_STREAM)
    serverSocket_TCP.bind(('', serverPort_TCP))
    serverSocket_TCP.listen(1)

    print("The server is ready to receive")
    while True:

        message, clientAddress = serverSocket_UDP.recvfrom(2048)
        response, trunc = UDP_SendQueryToResolver(message)
        print len(response)
        serverSocket_UDP.sendto(response, clientAddress)
        print 'UDP response sent.'
        if trunc:
            connectionSocket, addr = serverSocket_TCP.accept()
            print 'The TCP server is ready to receive'
            message = connectionSocket.recv(2048)
            response = TCP_SendQueryToResolver(message)
            print len(response)
            connectionSocket.send(response)
            print 'TCP response sent.'
            connectionSocket.close()


def UDP_SendQueryToResolver(message):
    serverName = "8.8.8.8"
    serverPort = 53
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message, (serverName, serverPort))
    response, serverAddress = clientSocket.recvfrom(2048)
    flag = response[2:4]
    flag = ''.join(format(ord(x), 'b') for x in flag)
    if flag[6] == '1':
        trunc = True
    else:
        trunc = False
    clientSocket.close()
    return response, trunc


def TCP_SendQueryToResolver(message):
    serverName = "8.8.8.8"
    serverPort = 53
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(message)
    response = ''
    while True:
        res = clientSocket.recv(2048)
        if not res:
            break
        response += res
    clientSocket.close()
    return response


if __name__ == "__main__":
    ReceiveQuery()
