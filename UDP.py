from socket import *
def ReceiveQuery():
    serverPort = 53
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('',serverPort))
    print( "The server is ready to receive")
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = SendQueryToResolver(message)
        flag = modifiedMessage[2:4]
        flag =''.join(format(ord(x), 'b') for x in flag)
        print flag
        serverSocket.sendto(modifiedMessage, clientAddress)



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
