#!/usr/bin/python
import socket


def get_request(socket):  # Receive the request from the client
    rqst = ''
    while True:
        data = socket.recv(2048)
        if not data:
            break
        rqst += data
        if rqst[-4:] == "\r\n\r\n":
            break
    return rqst


def response(sentence):  # generate http response message
    res = 'HTTP/1.0 200 OK\r\nConnection: close\r\n'
    hostname = parse(sentence)
    body = '<!DOCTYPE html>\n<html>\n<body>\n<p>I see you were looking for ' + hostname
    body += ', try this instead: <a href="http://stevetarzia.com">link</a>.</p>\n</body>\n</html>'
    res += 'Content-Length: ' + str(len(body))
    res += '\r\nContent-Type: text/html\r\n\r\n'
    res += body
    return res


def parse(sentence):  # parse http request and return the hostname
    hostname = sentence.split('\r\n')[1].split(' ')[1]
    return hostname


def connect(port):
    accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    accept_socket.bind(('', port))
    accept_socket.listen(5)
    print 'The server is ready to receive.'
    while True:
        connection_socket, addr = accept_socket.accept()
        rqst = get_request(connection_socket)
        if rqst != '':  # If rqst is null, the client connection is closed.
            res = response(rqst)
            connection_socket.send(res)
        connection_socket.close()
        print 'connection closed.'


if __name__ == '__main__':
    connect(80)
