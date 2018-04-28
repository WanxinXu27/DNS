from socket import *
def ReceiveQuery():
    serverPort = 53
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('',serverPort))
    print( "The server is ready to receive")
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        response, trunc = UDP_SendQueryToResolver(message)
        print "trunc" + str(trunc)
        if trunc == False:
            serverSocket.sendto(response, clientAddress)
        else:
            response = TCP_SendQueryToResolver(message)




def UDP_SendQueryToResolver(message):
    serverName = "8.8.8.8"
    serverPort = 53
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message, (serverName, serverPort))
    # print message
    # print "receive from 8.8.8.8:"
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
    # print message
    # print "receive from 8.8.8.8:"
    response = clientSocket.recv(2048)
    print response
    clientSocket.close()
    return response



if __name__ == "__main__":
    ReceiveQuery()
