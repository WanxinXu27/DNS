#!/usr/bin/python

from socket import *
import sys


def print_hex(response):  # debug purpose
    response = response.encode('hex')
    res = ''
    for i in range(len(response)):
        res += response[i]
        if i % 2:
            res += ' '
    return res


def change_nscount(responce):
    res1 = responce[0: 9]
    res3 = responce[10:]
    res2 = chr(0)
    res = res1 + res2 + res3
    return res


def change_ancount(response):  # answer RRs 0 -> 1
    res1 = response[0: 7]
    res3 = response[8:]
    res2 = chr(1)
    res = res1 + res2 + res3
    return res


def change_flag(response):  # RCODE -> 0000
    res1 = response[0: 3]
    res2 = response[3]
    res3 = response[4:]
    value = ord(res2)
    value -= 3
    res2 = chr(value)
    res = res1 + res2 + res3
    return res


def receive(socket):
    response = ''
    while True:
        res = socket.recv(2048)
        if not res:
            break
        response += res
    return response


def fabricate(response, ip):
    response = change_flag(response)
    response = change_ancount(response)
    response = change_nscount(response)
    pos = 0
    for i in range(len(response)):
        if response[i].encode('hex') == 'c0':
            pos = i
            break
    start = response[0: pos]
    ans = '\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x1a\x00\x04'
    ip = ip.split('.')
    for i in ip:
        ans += chr(int(i))
    res = start + ans
    return res


def check_flags(response):
    flag = get_flags_binary(response)
    if flag[6] == '1':
        trunc = True
    else:
        trunc = False
    if flag[-4:] == '0011':
        nerr = True
    else:
        nerr = False
    return trunc, nerr


def get_flags_binary(response):  # convert flag string to binary string
    flag = response[2:4]
    flag = ''.join(format(ord(x), 'b') for x in flag)
    return flag


def ReceiveQuery(ip):
    serverPort_UDP = 53
    serverSocket_UDP = socket(AF_INET, SOCK_DGRAM)
    serverSocket_UDP.bind(('', serverPort_UDP))

    serverPort_TCP = 53
    serverSocket_TCP = socket(AF_INET, SOCK_STREAM)
    serverSocket_TCP.bind(('', serverPort_TCP))
    serverSocket_TCP.listen(1)

    print "The server is ready to receive"
    while True:

        message, clientAddress = serverSocket_UDP.recvfrom(2048)
        response = UDP_SendQueryToResolver(message)
        print 'original response = ' + print_hex(response)
        trunc, nerr = check_flags(response)
        if nerr:
            print 'name error detected!'
            response = fabricate(response, ip)
            print 'fabricated response = ' + print_hex(response)
        serverSocket_UDP.sendto(response, clientAddress)
        print 'UDP response sent.\n'
        if trunc:
            connectionSocket, addr = serverSocket_TCP.accept()
            print 'The TCP server is ready to receive'
            message = connectionSocket.recv(2048)
            print 'message = ' + print_hex(message)
            response = TCP_SendQueryToResolver(message)
            connectionSocket.send(response)
            print 'response = ' + print_hex(response)
            print 'TCP response sent.\n'
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
    response = ''
    while True:
        res = clientSocket.recv(2048)
        if not res:
            break
        response += res
    clientSocket.close()
    return response


if __name__ == "__main__":
    ReceiveQuery(sys.argv[1])
