#! /usr/bin/env python

import sys
import socket
from datetime import datetime


def validateArgs(portArg):
    if len(sys.argv) != 2:
        print("usage: server.py <port_number>")

    if str.isdecimal(portArg):
        port = int(portArg)
        if port > 1024:
            print("port range: 1 - 1024")
    else:
        print("port is invalid")
    return port


def currentTime():
    # retrieve local time and return
    t = str(datetime.now())
    return t[0:19]


def logServerStatus(logData):
    # open log and record data
    log = open("sweet_chat_log.txt", "a")
    log.write(logData + "\r\n")
    log.close()


def getClientFD(clientFd):
    fd = clientFd.split()[1]
    fd = fd.split("=")[1]
    fd = fd[0:3]
    return str(fd)


def startServer():
    # defining connection message
    connectMsg = "┌───────────────────────┐\r\n│ Its Time to Chat Baby │\r\n└───────────────────────┘\r\n\r\n"

    # validate server port
    port = validateArgs(sys.argv[1])

    # creating, settings opts and binding to socket
    serverFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverFd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # serverFd.bind(("127.0.0.1", port))
    serverFd.bind(("192.168.210.105", port))

    # start listening
    print("server started successfully on " +  "127.0.0.1" + str(port) + " (\"CTRL + Break\" to stop)")
    logServerStatus("======================================\r\nServer started at: " + currentTime() + "\r\n======================================\r\n")
    serverFd.listen(1) #todo research listen(value)

    # awaiting client connections FOR.EV.VER
    while True:
        print("waiting for connection...")
        clientFd, addr = serverFd.accept()
        friendlyFd = getClientFD(str(clientFd))

        # accept connection and send connect msg
        print("connection received from " + addr[0] + ":"  + str(addr[1]) + " (" + friendlyFd + ") at " +currentTime())
        logServerStatus("connection received from " + addr[0] + ":"  + str(addr[1]) + " (" + friendlyFd + ") at " +currentTime())

        clientFd.sendall(connectMsg.encode("utf-8"))

        # while connected, echo received msgs
        while True:
            print("===========\r\nwaiting for data...")

            # receive and decode data
            data = clientFd.recv(1024)
            data = data.decode("utf-8")
            print("data received from (" + friendlyFd + ") at " +currentTime())
            logServerStatus("data received from " + addr[0] + ":" + str(addr[1]) + " (" + friendlyFd + ") at " + currentTime())

            # if "quit" recv'd, close connection and shutdown
            if data == "quit":
                clientFd.shutdown(1)
                clientFd.close()
                print("closing connection to " + addr[0] + ":"  + str(addr[1]) + " (" + friendlyFd + ") at " +currentTime())
                logServerStatus("closing connection to " + addr[0] + ":"  + str(addr[1]) + " (" + friendlyFd + ") at " +currentTime() + "\r\n")
                break
            # else, encode and send data
            elif data:
                clientFd.sendall(data.encode("utf-8"))


if __name__ == '__main__':
    startServer()

