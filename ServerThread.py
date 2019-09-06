#This is a basic server side program, runs wiithout error but my ports arn't forwarding so I can't connect with client yet
#Searching on campus for open ports to test this on

import socket
import threading
import sys
import os
import time
import pickle
import re
from userDB import User
from os.path import expanduser, join

class Room:
    def __init__(self,name):
        self.name = name
        self.users = [] # List of connections
        self.user_ids = []
        self.active_users = {}

    def add_user(self, conn, user_id):
        self.users.append(conn)
        self.user_ids.append(user_id)
        self.active_users[user_id] = conn

    def remove_user(self, conn):
        client_userID = ""

        for user_id, connection in self.active_users.items():
            if(conn == connection):
                client_userID = user_id

        self.users.remove(conn)

        if(client_userID != ""):
            self.user_ids.remove(client_userID)

        self.active_users.pop(client_userID)

class Server:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("server IP: " + socket.gethostname())
    
    rooms = {}
    rooms["General"] = Room("General") # was connections
    
    #General chat history
    parent_dir = os.getcwd()
    directory = os.path.join(parent_dir, "chat_histories")
    if not os.path.exists(directory):
        os.makedirs(directory)

    hFile = os.path.join(directory, "General.txt")
    f= open(hFile, "a+")
    f.flush()
    f.close()

    def __init__(self):
        self.soc.bind(('0.0.0.0', 7290)) #IP and port
        self.soc.listen(1)

    def handler(self, conn, addr): #handle user messages and commands from the client
        error = False
        logout = False
        run = True
        while run:
            data = bytes('Identifier', 'utf-8')
            try:
                data = conn.recv(1024) #buffer size of 1024 bytes
            except:
                error = True

            if (data.split(b' ')[0] == bytes('/logout', 'utf-8')):
                logout = True

            elif (data.split(b' ')[0] == bytes('/quit', 'utf-8')) or error: #CHANGE THIS TO ACT LIKE changeGroup. Have a quit button
                print(str(addr[0]) + ':' + str(addr[1]), "disconnected")
                for r in self.rooms:
                    if conn in self.rooms[r].users:
                        self.rooms[r].remove_user(conn)
                        if error:
                            for connection in self.rooms[r].users: #send data to all members connected. In the future make this a que to send all message history
                                connection.send(bytes("So long! A user has left the chat. Active users: " + str(len(self.rooms[r].users)) +"\n", 'utf-8'))
                        else:
                            for connection in self.rooms[r].users: #send data to all members connected. In the future make this a que to send all message history
                                connection.send(bytes("So long! " +str(data.split(b' ')[1], 'utf-8')+ " has left the chat. Active users: " + str(len(self.rooms[r].users)) + '\n', 'utf-8'))    
                        conn.close()
                        run = False
                        break       
                    
            elif data.split(b' ')[0] == bytes('/login', 'utf-8'):
                user_name = str(data.split(b' ')[1], 'utf-8')
                user_id = str(data.split(b' ')[3], 'utf-8')

                newGroup = "General"
                newRoom = Room(newGroup)
                self.rooms[newGroup] = newRoom
                self.rooms[newGroup].add_user(conn, user_id)

                for connection in self.rooms[newGroup].users:
                    connection.send(bytes(str(data.split(b' ')[1], 'utf-8')+ " has joined the group. Active users: " + str(len(self.rooms[newGroup].users)), 'utf-8'))
                    time.sleep(.001)

                parent_dir = os.getcwd()
                directory = os.path.join(parent_dir, "chat_histories")
                fName = "General.txt"
                hFile = os.path.join(directory, fName)
                f= open(hFile, "r")
                for line in f:
                    conn.send(bytes(line, 'utf-8')) #send history
                    time.sleep(.001)

                f.close()

            elif data.split(b' ')[0] == bytes('/joinGroup', 'utf-8'):
                break

            elif data.split(b' ')[0] == bytes('/changeGroup', 'utf-8'):
                newGroup = str(data.split(b' ')[2], 'utf-8')
                user_id = str(data.split(b' ')[3], 'utf-8')

                if len(data.split(b' ')) > 4:
                    for x in range(0,len(data.split(b' '))-4):
                        newGroup = newGroup + " " + str(data.split(b' ')[4+x], 'utf-8')
                #also check if already in the room
                if newGroup in self.rooms: #switch to an existing room
                    for r in self.rooms:
                        if conn in self.rooms[r].users:
                            self.rooms[r].remove_user(conn)
                            for connection in self.rooms[r].users: #send data to all members connected. In the future make this a que to send all message history
                                connection.send(bytes("So long! " +str(data.split(b' ')[1], 'utf-8')+ " has left the group. Active users: " + str(len(self.rooms[r].users))+"\n", 'utf-8'))
                    self.rooms[newGroup].add_user(conn, user_id)
                    
                    parent_dir = os.getcwd()
                    directory = os.path.join(parent_dir, "chat_histories")
                    print("Saving File $1: ")
                    print(newGroup)
                    fName = newGroup+".txt"
                    hFile = os.path.join(directory, fName)
                    f = open(hFile, "r")
                    
                    for line in f:
                        conn.send(bytes(line, 'utf-8')) #send history
                        time.sleep(.001)
                    for connection in self.rooms[newGroup].users:
                        if connection != conn:
                            connection.send(bytes(str(data.split(b' ')[1], 'utf-8')+ " has joined the group. Active users: " + str(len(self.rooms[newGroup].users))+"\n", 'utf-8'))
                            time.sleep(.001)
                else: #switch to a brand new room
                    for r in self.rooms:
                        if conn in self.rooms[r].users:
                            self.rooms[r].remove_user(conn)
                            for connection in self.rooms[r].users: #send data to all members connected. In the future make this a que to send all message history
                                connection.send(bytes("So long! " +str(data.split(b' ')[1], 'utf-8')+ " has left the group. Active users: " + str(len(self.rooms[r].users))+"\n", 'utf-8'))
                    
                    newRoom = Room(newGroup)
                    self.rooms[newGroup] = newRoom
                    self.rooms[newGroup].add_user(conn, user_id)
                    conn.send(bytes(str(data.split(b' ')[1], 'utf-8')+ " has joined the group. Active users: " + str(len(self.rooms[newGroup].users))+"\n", 'utf-8'))
                
                    parent_dir = os.getcwd()
                    directory = os.path.join(parent_dir, "chat_histories")
                    print(newGroup)
                    print("Saving File @2: ")
                    fName = newGroup+".txt"
                    hFile = os.path.join(directory, fName)
                    f= open(hFile, "a+")
                    f.close()

            elif data.split(b' ')[0] == bytes('/updateGroupLists', 'utf-8'):
                #groupData = conn.recv(1024)
                group_members = pickle.loads(data.split(b' ')[1])

                for member_id in group_members:
                    for r in self.rooms:
                        for user_id, user_conn in self.rooms[r].active_users.items():
                            print(user_id)
                            if member_id[0] == user_id:
                                user_conn.send(bytes('/updateClient', 'utf-8'))

            else:
                #check which group the user is in by searching through the lists and then print to tha group
                for r in self.rooms:
                    if conn in self.rooms[r].users:
                        group = self.rooms[r].name
                        break
                for connection in self.rooms[group].users: #send data to all members connected. In the future make this a que to send all message history
                    connection.send(bytes(data))
                    #write to a file for history

                #tkmsg = self.with_surrogates(data.decode()+"\n")
                parent_dir = os.getcwd()
                directory = os.path.join(parent_dir, "chat_histories")
                fName = group+".txt"

                hFile = os.path.join(directory, fName)
                try:
                    with open(hFile, "a+") as txt_file:
                
                    #data.decode()
                        txt_file.write(data.decode() + '\n')
                        txt_file.flush()
                        txt_file.close()
                except:
                    pass
                
    def run(self):
        while True:
            conn, addr = self.soc.accept()
            cThread = threading.Thread(target=self.handler, args=(conn,addr))
            cThread.daemon = True #allows for closeing while thread is still running
            cThread.start()
            print(str(addr[0]) + ':' + str(addr[1]), "connected")

server = Server()
server.run()