#!/usr/bin/python

from socket import *


def change_flag(response):  # change RCODE to 0000
    res1 = response[0: 2]
    res2 = get_flags(response)  # flags in binary
    res3 = response[4:]
    temp = list(res2)
    temp[-1] = '0'  # change RCODE to 0000
    res2 = ''.join(temp)
    response = res1 + res2 + res3
    return response


def receive(socket):
    response = ''
    while True:
        res = socket.recv(2048)
        if not res:
            break
        response += res
    return response


def fabricate(response):
    response = change_flag(response)
    pos = 0
    for i in range(len(response)):
        if response[i].encode('hex') == 'c0':
            pos = i
            break
    start = response[0: pos]
    ans = 'c00c000100010000001a000412de3b96'
    ans = ans.decode('hex')
    response = start + ans
    return response


def check_flags(response):
    flag = get_flags(response)
    if flag[6] == '1':
        trunc = True
    else:
        trunc = False
    if flag[-4:] == '0011':
        nerr = True
    else:
        nerr = False
    return trunc, nerr


def get_flags(response):
    flag = response[2:4]
    flag = ''.join(format(ord(x), 'b') for x in flag)
    return flag


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
        response = UDP_SendQueryToResolver(message)
        trunc, nerr = check_flags(response)
        print len(response)
        if nerr:
            response = fabricate(response)
            print response
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
    clientSocket.close()
    return response


def TCP_SendQueryToResolver(message):
    serverName = "8.8.8.8"
    serverPort = 53
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(message)
    response = receive(clientSocket)
    clientSocket.close()
    return response


if __name__ == "__main__":
    ReceiveQuery()
