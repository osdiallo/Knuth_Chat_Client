#Basic client side of the server program, haven't tested because my ports aren't forwarded yet. 
#So far it keeps track of who is connected and the messages are printed out only to those who are online.
#Still need to add in names of who sent the message, a history so you can see messages when you weren't online, and more.

import socket
import threading
import sys
import re
#import controller
#from view import ChatPage
from tkinter import *
from userDB import User
import pickle

class Client:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def sendMsg(self, controller, User):
        mes = bytes(controller.page.inputField.get(), 'utf-8')
        #add commands in here to client side
        if mes == bytes('/quit', 'utf-8'): #handles a quit command and relays the username to the server
            controller.soc.send(mes+bytes(" "+User.name, 'utf-8'))
        else:
            controller.page.msgList.configure(state=NORMAL)
            controller.soc.send(bytes(User.name + ": ", 'utf-8')+mes) #adds the name to the message
            controller.page.msgList.configure(state=DISABLED)

    def changeGroup(self, controller, User, group):
        controller.soc.send(bytes("/changeGroup "+User.name+" "+group+" "+User.id, 'utf-8'))
    
    def loginUser(self, controller, User, group):
        controller.soc.send(bytes("/login "+User.name+" "+group+" "+User.id, 'utf-8'))

    def logoutUser(self, controller, User, group):
        controller.soc.send(bytes("/logout "+User.name+" "+group, 'utf-8'))

    def updateAllGroupMembers(self, controller, members_of_group):
        currentGroupInfo = pickle.dumps(members_of_group)
        controller.soc.send(bytes("/updateGroupLists ", 'utf-8')+bytes(currentGroupInfo))

    def __init__(self, controller, User, address):
        self.soc.connect((address, 7290)) #ip and port
        controller.soc = self.soc
        controller.updateAllLists()

        while True: #for incoming messages
            controller.page.msgList.tag_configure("user", background=controller.currentUser.textbg)
            controller.page.msgList.tag_configure("non-user", background="White")

            data = self.soc.recv(1024) #buffer size of 1024 bytes
            if not data:
                break
            #need to make this add text to the window

            if(data.split(b' ')[0] == bytes('/updateClient', 'utf-8')):
                controller.updateAllLists()
                continue

            try:
                controller.page.msgList.configure(state=NORMAL)
                controller.page.msgList.insert(END, str(data.decode()+'\n'))
                controller.page.msgList.configure(state=DISABLED)
                s = str(data).split(":", 1)
                s[0] = s[0][2:]
                line, c = map(int, controller.page.msgList.index("end-1c").split("."))

                for i in range(1, int(line)):
                    user_len = len(controller.currentUser.name)
                    pre_fix = controller.currentUser.name+":"

                    if(controller.page.msgList.get("%s.0" % i, "%s.%d" % (i, user_len+1)) == pre_fix):
                        tag = "user"
                        controller.page.msgList.tag_add(tag, "%s.0" % (i), "%s.end" % i)
                    if(controller.page.msgList.get("%s.0" % i, "%s.%d" % (i, user_len+1)) != pre_fix):
                        tag = "non-user"
                        controller.page.msgList.tag_add(tag, "%s.0 wordstart" % (i), "%s.end" % i)

            except:
                pass

            controller.page.msgList.see(END)

#client = Client('Ace') #put ip address of the server here