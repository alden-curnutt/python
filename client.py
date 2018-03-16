#! /usr/bin/env python

import sys
import socket

def validateArgs():
    # validating arg count
    if len(sys.argv) != 3:
        print("usage client.py <ip_address> <port>")
        return False

    # Validating ip address, exit
    # script if address is invalid
    try:
        socket.inet_aton(sys.argv[1])
    except socket.error:
        print("invalid ip address")
        exit(1)

    # Validating port number, exit
    # if port is invalid
    if str.isdecimal(sys.argv[2]):
        port = int(sys.argv[2])
        if port > 1024:
            print("port range: 1 - 1024")
            exit(1)
    else:
        print("port is invalid")
    return port

# validate port number
port = validateArgs()

# creating socket file descriptor
serverFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddy = (sys.argv[1], 1024)

# attempting connection to server
print("Attempting connecting to " + str(sys.argv[1]) + ":" + str(port) + "...")
try:
    serverFd.connect(serverAddy)
except ConnectionRefusedError:
    print("connection refused, exiting script")
    exit(1)
except OSError: #todo research if this is needed
    print("address is not valid, exiting script")
    exit(1)
print("Successful connection to server @" + str(sys.argv[1]) + ":" + str(port))

# receive and print connect msg from server
message = serverFd.recv(1024).decode()
print(message)

# while connected, chat 'er up
while True:
    data = input("Type your message:\r\n> ")
    if data == "quit":
        serverFd.sendall(data.encode("utf-8"))
        print("server has disconnected. exiting...")
        break
    else:
        print("Sending: " + data)

        try:
            serverFd.sendall(data.encode("utf-8"))
        except ConnectionResetError:
            break

        echo = serverFd.recv(1024).decode()
        print("Received: " + str(echo))



# closing connection to server
print("bye felicia")
serverFd.close()







