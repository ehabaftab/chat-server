#!/bin/python
import signal
import os
import sys
import socket
import select
import hashlib
import time

HOST = '' 
SOCKET_LIST = []
channels = []
users = []
logged_in = []
usernames = []
registered = []
RECV_BUFFER = 4096 
if(len(sys.argv) < 2) :
    print('Usage : python chat.py port')
    sys.exit()

PORT = int(sys.argv[1])
#database = "test.csv"
database = {}

#Use this variable for your loop
daemon_quit = False

#Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True



def run():
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    # Call your own functions from within 
    # the run() funcion
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print("Chat server started on port " + str(PORT))
    while not daemon_quit:
        #f = open(database, 'a+')
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("Client (%s, %s) connected" % addr)
                 
                #broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    decoded_data = data.decode().strip()
                    if data:
                        # there is something in the socket
                        if(decoded_data.split()[0] == 'REGISTER'):
                            register(decoded_data,sock)
                        elif(decoded_data.split()[0] == 'LOGIN'):
                            success = login(decoded_data,sock)
                            if success:
                                logged_in.append(sock)
                                usernames.append(decoded_data.split()[1])
                        elif(decoded_data.split()[0] == 'CHANNELS'):  
                            list_channels(sock)

                        elif sock in logged_in:
                            if(decoded_data.split()[0] == 'CREATE'):
                                create_channel(decoded_data,sock)
                            elif(decoded_data.split()[0] == 'JOIN'):
                                join_channel(decoded_data,sock)
                            elif(decoded_data.split()[0] == 'SAY'):
                                broadcast(server_socket, sock, decoded_data)
                            elif(decoded_data.split()[0] == 'CHANNELS'):  
                                list_channels(sock)
                            else:
                                sock.send("INVALID COMMAND\n".encode())
                        else:
                            sock.send("INVALID COMMAND\n".encode())
                            
                    else:
                        # signs out the socket that has disconnected
                        for i in range(len(logged_in)):
                            if sock == logged_in[i]:
                                logged_in.remove(sock)
                                usernames.pop(i)
                        # removes the socket that has disconnected from the channel
                        for i in range(len(channels)):
                            if sock in users[i]:
                                users[i].remove(sock)
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        print(str(sock.getpeername()) + " DISCONNECTED")

                except:
                    continue
    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, data):
    members = []
    if len(data.split()) < 2:
        sock.send("INVALID\n".encode())
        return
    channel = data.split()[1]
    message = " ".join(data.split()[2:])
    for j in range(len(logged_in)):
        if logged_in[j] == sock:
            name = usernames[j]
    for i in range(len(channels)):
        if channels[i] == channel:
            members = users[i]
    # if the user is not part of the channel
    if len(members) == 0:
        sock.send("NOT SUBSCRIBED\n".encode())
        return
    for socket in members:
        socket.send("RECV {} {} {}\n".format(name,channel,message).encode())
 
def register(data,sock):
    if len(data.split()) < 3:
        sock.send("RESULT REGISTER 0\n".encode())
        return
    if data.split()[1] in registered:
        sock.send("RESULT REGISTER 0\n".encode())
        return
    database[data.split()[1]] = hashlib.sha256(data.split()[2].encode()).hexdigest()
    sock.send("RESULT REGISTER 1\n".encode())
    registered.append(data.split()[1])
    

def login(data,sock):
    if len(data.split()) < 3:
        sock.send("RESULT LOGIN 0\n".encode())
        return
    if database.get(data.split()[1]) == hashlib.sha256(data.split()[2].encode()).hexdigest() and data.split()[1] not in usernames:
        if sock in logged_in:
            sock.send("RESULT LOGIN 0\n".encode())
            return False
        sock.send("RESULT LOGIN 1\n".encode())
        return True
    else:
        sock.send("RESULT LOGIN 0\n".encode())
        return False


def create_channel(data,sock):
    if len(data.split()) < 2:
        sock.send("INVALID\n".encode())
        return
    name = " ".join(data.split()[1:])
    if name not in channels:
        channels.append(name)
        users.append(list(''))
        sock.send("RESULT CREATE {} 1\n".format(name).encode())
    else:
        sock.send("RESULT CREATE {} 0\n".format(name).encode())

def join_channel(data,sock):
    if len(data.split()) < 2:
        sock.send("INVALID\n".encode())
        return
    name = " ".join(data.split()[1:])
    if len(channels) == 0:
        sock.send("RESULT JOIN {} 0\n".format(name).encode())
    else:
        for i in range(len(channels)):
            if channels[i] == name:
                # if the user is not already the part of the channel
                if sock not in users[i]:
                    users[i].append(sock)
                else:
                    sock.send("RESULT JOIN {} 0\n".format(name).encode())
                    return
                sock.send("RESULT JOIN {} 1\n".format(name).encode())
                
                return
        sock.send("RESULT JOIN {} 0\n".format(name).encode())
            
def list_channels(sock):
    channels.sort()
    sock.send("RESULT CHANNELS {}\n".format(", ".join(channels)).encode())


if __name__ == '__main__':
    run()