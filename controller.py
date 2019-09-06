# Controller file to read from view and communicate
# with model class to update the view
from model import *
from view import *
from tkinter import *
import userDB
import threading
from ClientThread import *
from userDB import User
from userDB import Group
import os

class Controller(Tk):

    #class constructor
    def __init__(self):
        Tk.__init__(self)
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        self.currentUser = User() #None
        self.currentGroup = Group()
        self.realColor = "SeaGreen3"

        self.accSettingsOpen = None
        self.groupSettingsOpen = None
        self.createGroupOpen = None
        self.joinGroupOpen = None
        self.addFriendOpen = None
        self.pages = {}
        self.userIP = 'Oumar-UltraBook'
        self.newLog = 0

        for F in (LoginPage, ChatPage, RegistrationPage, FRegistrationPage):
            self.page = F(self.container, self)
            self.pages[F] = self.page
            self.page.grid(row=0,column=0,sticky="nsew")
            
        self.switch_page(LoginPage)
        self.model = Model()

    def switch_page(self, page_class):
        self.page = self.pages[page_class]
        self.page.tkraise()

        if(page_class == LoginPage): # Resizes and centers page
            windowWidth = 230
            windowHeight = 250
            self.title("Log In")
        
        if(page_class == RegistrationPage): # Resizes and centers page
            windowWidth = 270
            windowHeight = 280
            self.title("Registration Page")

        if(page_class == FRegistrationPage):
            windowWidth = 240
            windowHeight = 250
            self.title("Forgotten Username/Email")

        if(page_class == ChatPage): # Resizes and centers page
            windowWidth = 605
            windowHeight = 520
            self.title("Knuth Konnections")

        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/3 - windowHeight/2)
        self.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))

    def accSettingsButtonClick(self):
        if(self.accSettingsOpen == None):
            self.accSettingsOpen = AccSettingsPopup(self.page, self)

    def groupSettingsButtonClick(self):
        if(self.groupSettingsOpen == None):
            self.groupSettingsOpen = GroupSettingsPopup(self.page, self)

    def createNewGroupClick(self):
        if(self.createGroupOpen == None):
            self.createGroupOpen = CreateGroupPopup(self.page, self)

    def joinNewGroupClick(self):
        if(self.joinGroupOpen == None):
            self.joinGroupOpen = JoinGroupPopup(self.page, self)

    def addNewFriend(self):
        if(self.addFriendOpen == None):
            self.addFriendOpen = AddFriendPopup(self.page, self)

    def Textbg(self, AccSettingsPopup):
        self.currentUser.textbg = AccSettingsPopup.defaultV.get()
        userDB.update_user_info(AccSettingsPopup.defaultV.get(), 'textbg', self.currentUser.id)
        self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')

    def changeTheme(self, AccSettingsPopup):
        self.newtheme = AccSettingsPopup.defaultVal.get()
        self.changeColors(self.newtheme, AccSettingsPopup)

    def changeColors(self, color, AccSettingsPopup = None):
        if(color == "Green"):
            self.realColor = "SeaGreen3"
        if(color == "Blue"):
            self.realColor = "RoyalBlue3"
        if(color == "Red"):
            self.realColor = "red3"
        if(color == "Orange"):
            self.realColor = "DarkOrange1"

        if(AccSettingsPopup != None):
            AccSettingsPopup.window.config(background=self.realColor)
            AccSettingsPopup.errLabel.config(background=self.realColor)
            AccSettingsPopup.themeInstruction.config(background=self.realColor)
            AccSettingsPopup.textInstruction.config(background=self.realColor)
            AccSettingsPopup.confirmInstruction.config(background=self.realColor)
            AccSettingsPopup.passInstruction.config(background=self.realColor)
            AccSettingsPopup.emailInstruction.config(background=self.realColor)
            AccSettingsPopup.userInstruction.config(background=self.realColor)
            AccSettingsPopup.oldPassLabel.config(background=self.realColor)
            AccSettingsPopup.title.config(background=self.realColor)
            AccSettingsPopup.themeDropDown.config(highlightbackground=self.realColor)
            AccSettingsPopup.theDropDown.config(highlightbackground=self.realColor)

        self.page.config(background=self.realColor)
        self.page.messages.config(background=self.realColor)
        self.page.inputFrame.config(background=self.realColor)
        self.page.groups.config(background=self.realColor)
        self.page.groupListLabel.config(background=self.realColor)
        self.page.knuthKonnectionsLabel.config(background=self.realColor)
        self.page.groupListFrame.config(background=self.realColor)
        self.page.groupNameFrame.config(background=self.realColor)
        #self.page.groupName.config(background=self.realColor)
        self.page.settingsFrame.config(background=self.realColor)

        userDB.update_user_info(color, 'theme', self.currentUser.id)

    def changeUserAndPass(self, AccSettingsPopup):
        self.accSettingsOpen.errLabel.config(text="", foreground="red")
        self.newuser = ""
        self.newpass = ""
        self.newemail = ""
        self.olduser = self.currentUser.name
        self.oldemail = self.currentUser.email
        self.oldpass = AccSettingsPopup.oldPassEntry.get()
        self.currentID = self.currentUser.id

        #Check for valid password, if it is valid, we can change settings
        if(userDB.login_user(self.currentUser.name, self.oldpass) == 2):
            self.accSettingsOpen.errLabel.config(text="Invalid Password!")
            return
        else:
            # Check new password input
            if AccSettingsPopup.changePasswordInput.get() != "":
                if AccSettingsPopup.confirmPasswordInput.get() != AccSettingsPopup.changePasswordInput.get():
                    self.accSettingsOpen.errLabel.config(text="New Password does not match confirmation")
                    return
                else:
                    #if new passwords match, set newpass
                    self.newpass = AccSettingsPopup.changePasswordInput.get()
                    self.accSettingsOpen.errLabel.config(text="Settings Changed", foreground="green")  
                    userDB.update_user_info(self.newpass, 'password', self.currentUser.id)
                    self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')

            # Check new email input
            if AccSettingsPopup.changeEmailInput.get() !="":
                self.newemail = AccSettingsPopup.changeEmailInput.get()

                if(self.newemail == self.oldemail):
                    self.accSettingsOpen.errLabel.config(text="E-Mail unchanged", foreground="yellow")
                if(userDB.check_valid_email(self.newemail) == None):
                    self.accSettingsOpen.errLabel.config(text="E-Mail already registered", foreground="green")
                    return
                elif(userDB.check_valid_email(self.newemail) == True):
                    userDB.update_user_info(self.newemail, 'email', self.currentUser.id)
                    #self.currentUser = userDB.load_user_info(None, self.currentUser.id[0], 'user_id')
                else:
                    self.accSettingsOpen.errLabel.config(text="Invalid or already registered E-Mail Address.")
                    return

            #Check username input
            if AccSettingsPopup.changeUserNameInput.get() != "":
                self.newuser = AccSettingsPopup.changeUserNameInput.get()

                if(self.newuser == self.olduser):
                    self.accSettingsOpen.errLabel.config(text="Username unchanged", foreground="yellow")
                    return
                
                if(userDB.checkAccExistence(self.newuser, 'username')): #if the new username is already registered
                    self.accSettingsOpen.errLabel.config(text="Username is already taken.\nPlease choose a different username")
                    return

                userDB.update_user_info(self.newuser, 'username', self.currentUser.id, self.olduser)
                self.accSettingsOpen.errLabel.config(text="Settings Changed", foreground="green")
                Client.updateAllGroupMembers(self, self, self.currentUser.friends)

        #Call changes with updated information  
        self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')   

    def click(self, event): #handles click for username
        if self.page.Name_entry.get() == "Username":
            self.page.Name_entry.delete(0, "end")
            self.page.Name_entry.insert(0, "")
            self.page.Name_entry.config(fg = "black")

    def clickP(self, event): #handles click for Password
        if self.page.Pass_entry.get() == "Password":
            self.page.Pass_entry.delete(0, "end")
            self.page.Pass_entry.insert(0, "")
            self.page.Pass_entry.config(fg = "black", show="*")

    def clickCU(self, event): #handles click for creating username
        if self.page.Name_entry.get() == "Create a Username":
            self.page.Name_entry.delete(0, "end")
            self.page.Name_entry.insert(0, "")
            self.page.Name_entry.config(fg = "black")

    def clickFE(self, event): #handles click for creating username
        if self.page.email_entry.get() == "Enter your email":
            self.page.email_entry.delete(0, "end")
            self.page.email_entry.insert(0, "")
            self.page.email_entry.config(fg = "black")

    def clickCE(self, event): #handles clicking for specifying email
        if self.page.email_entry.get() == "Enter Your E-Mail":
            self.page.email_entry.delete(0, "end")
            self.page.email_entry.insert(0, "")
            self.page.email_entry.config(fg = "black")

    def clickCP(self, event): #handles click for creating user password
        if self.page.Pass_entry.get() == "Choose a Password":
            self.page.Pass_entry.delete(0, "end")
            self.page.Pass_entry.insert(0, "")
            self.page.Pass_entry.config(fg = "black", show="*")

    def clickCRP(self, event): #handles click for the re-entry of user created password
        if self.page.Pass_reentry.get() == "Re-Enter Password":
            self.page.Pass_reentry.delete(0, "end")
            self.page.Pass_reentry.insert(0, "")
            self.page.Pass_reentry.config(fg = "black", show="*")

    def clickIF(self, event): # Handles clicking into the input message field.
        if self.page.inputField.get() == "Click here to type":
            self.page.inputField.delete(0, "end")
            self.page.inputField.insert(0, "")
            self.page.inputField.config(fg="black")

    def clickCGN(self, event): # Handles clicking into creating group name field
        if self.createGroupOpen.new_group_name.get() == "New Group Name":
            self.createGroupOpen.new_group_name.delete(0, "end")
            self.createGroupOpen.new_group_name.insert(0, "")
            self.createGroupOpen.new_group_name.config(fg="black")

    def clickJGN(self, event): # Handles clicking into joining group name field
        if self.joinGroupOpen.join_group_id.get() == "Enter Group ID":
            self.joinGroupOpen.join_group_id.delete(0, "end")
            self.joinGroupOpen.join_group_id.insert(0, "")
            self.joinGroupOpen.join_group_id.config(fg="black")

    def clickNFN(self, event): # Handles clicking into the add new friend field
        if self.addFriendOpen.new_friend_name.get() == "Search For User...":
            self.addFriendOpen.new_friend_name.delete(0, "end")
            self.addFriendOpen.new_friend_name.insert(0, "")
            self.addFriendOpen.new_friend_name.config(fg="black")

    def clickout(self, event): #handles clicking out of username
        if self.page.Name_entry.get() == "":
            self.page.Name_entry.insert(0, "Username")
            self.page.Name_entry.config(fg = "grey")

    def clickoutP(self, event): #handles clicking out of password
        if self.page == LoginPage:
            if self.page.Pass_entry.get() == "":
                self.page.Pass_entry.insert(0, "Password")
                self.page.Pass_entry.config(fg = "grey", show="")

    def clickoutCU(self, event): #handles clicking out of creating username
        if self.page.Name_entry.get() == "":
            self.page.Name_entry.insert(0, "Create a Username")
            self.page.Name_entry.config(fg = "grey")

    def clickoutFE(self, event): #handles clicking out of creating username
        if self.page.email_entry.get() == "":
            self.page.email_entry.insert(0, "Enter your email")
            self.page.email_entry.config(fg = "grey")

    def clickoutCE(self, event): #handles clicking out of specifying email
        if self.page.email_entry.get() == "":
            self.page.email_entry.insert(0, "Enter Your E-Mail")
            self.page.email_entry.config(fg = "grey")

    def clickoutCP(self, event): #handles clicking out of creating user password
        if self.page.Pass_entry.get() == "":
            self.page.Pass_entry.insert(0, "Choose a Password")
            self.page.Pass_entry.config(fg = "grey", show="")

    def clickoutCRP(self, event): #handles clicking out of re-creating user password
        if self.page.Pass_reentry.get() == "":
            self.page.Pass_reentry.insert(0, "Re-Enter Password")
            self.page.Pass_reentry.config(fg = "grey", show="")

    def clickoutIF(self, event): # Handles clicking out of the input message field.
        if self.page.inputField.get() == "":
            self.page.inputField.insert(0, "Click here to type")
            self.page.inputField.config(fg="grey")

    def clickoutCGN(self, event): # handles clicking out of creating group name field
        if self.createGroupOpen.new_group_name.get() == "":
            self.createGroupOpen.new_group_name.insert(0, "New Group Name")
            self.createGroupOpen.new_group_name.config(fg="grey")

    def clickoutJGN(self, event): # Handles clicking out of joining group name field
        if self.joinGroupOpen.join_group_id.get() == "":
            self.joinGroupOpen.join_group_id.insert(0, "Enter Group ID")
            self.joinGroupOpen.join_group_id.config(fg="grey")

    def clickoutNFN(self, event): # Handles clicking out of the add new friend field
        if self.addFriendOpen.new_friend_name.get() == "":
            self.addFriendOpen.new_friend_name.insert(0, "Search For User...")
            self.addFriendOpen.new_friend_name.config(fg="grey")

    def logOutClick(self):
        if(self.accSettingsOpen != None):
            AccSettingsPopup.destroyPopup(self.accSettingsOpen)

        if(self.groupSettingsOpen != None):
            GroupSettingsPopup.destroyPopup(self.groupSettingsOpen)

        if(self.createGroupOpen != None):
            CreateGroupPopup.destroyPopup(self.createGroupOpen)

        if(self.joinGroupOpen != None):
            JoinGroupPopup.destroyPopup(self.joinGroupOpen)

        Client.logoutUser(self, self, self.currentUser, self.page.currentGroupTitle.get(),)
        self.currentUser = None
        self.currentGroup = None
        self.switch_page(LoginPage)
    
    def logInClick(self): # loads a user and their groups on a successful login
        if((self.page.Name_entry.get() == "") or (self.page.Pass_entry.get() == "") or (self.page.Name_entry.get() == "Username") or (self.page.Pass_entry.get() == "Password")):
            self.page.elabel.config(text="Incomplete Sign In!")
        elif(userDB.login_user(self.page.Name_entry.get(), self.page.Pass_entry.get()) == 0):
            self.page.elabel.config(text="You are not currently registered!\n Please Register first.")
        elif(userDB.login_user(self.page.Name_entry.get(), self.page.Pass_entry.get()) == 1):
            self.page.elabel.config(text="")
            self.currentUser = userDB.load_user_info(self.page.Name_entry.get())

            # unless the user checks 'Remember Me', delete text entries
            if(self.page.rememberUser.get() == 0):
                self.page.Name_entry.delete(0, 'end')
                self.page.Pass_entry.delete(0, 'end')

            self.switch_page(ChatPage)
            self.page.initGroupList(self.currentUser.groups)
            self.page.initFriendList(self.currentUser)
            self.changeColors(self.currentUser.theme)

            if self.newLog is 0:
                self.client = threading.Thread(target=Client, args=(self, self.currentUser, self.userIP,))
                self.client.daemon = True
                self.client.start()

            self.currentGroup = userDB.load_group_info('00000000')
            self.page.updateGroupList(self.currentUser.groups)
            self.page.updateFriendList(self.currentUser)
            self.ChangeGroupChat(self.currentGroup.id, login=True)

        elif(userDB.login_user(self.page.Name_entry.get(), self.page.Pass_entry.get()) == 2):
            self.page.elabel.config(text="Login Information Invalid!")

    def enterP(self, event): # Registers 'enter' as a way to sign in.
        self.page.sin.focus_set()
        if((self.page.Name_entry.get() == "") or (self.page.Pass_entry.get() == "") or (self.page.Name_entry.get() == "Username") or (self.page.Pass_entry.get() == "Password")):
            self.page.elabel.config(text="Incomplete Sign In!")
        elif(userDB.login_user(self.page.Name_entry.get(), self.page.Pass_entry.get()) == 0):
            self.page.elabel.config(text="You are not currently registered!\n Please register first.")
        elif(userDB.login_user(self.page.Name_entry.get(), self.page.Pass_entry.get()) == 1):
            self.page.elabel.config(text="")
            self.currentUser = userDB.load_user_info(self.page.Name_entry.get())
            
            if(self.page.rememberUser.get() == 0):
                self.page.Name_entry.delete(0, 'end')
                self.page.Pass_entry.delete(0, 'end')
            
            self.switch_page(ChatPage)
            self.page.initGroupList(self.currentUser.groups)
            self.page.initFriendList(self.currentUser)
            self.changeColors(self.currentUser.theme)

            if self.newLog is 0:
                self.client = threading.Thread(target=Client, args=(self, self.currentUser, self.userIP,))
                self.client.daemon = True
                self.client.start()

            self.currentGroup = userDB.load_group_info('00000000')
            self.page.updateGroupList(self.currentUser.groups)
            self.page.updateFriendList(self.currentUser)
            self.ChangeGroupChat(self.currentGroup.id, login=True)

        elif(userDB.login_user(self.page.Name_entry.get(), self.page.Pass_entry.get()) == 2):
            self.page.elabel.config(text="Login Information Invalid!")

    def registerClick(self):
        self.switch_page(RegistrationPage)

    def completeRegClick(self):
        login_user = 0

        if(self.page.Name_entry.get() == "" or 
           self.page.Name_entry.get() == "Create a Username"):
            self.page.flabel.config(text="Please enter a username.")
            return
        
        if(userDB.checkAccExistence(self.page.Name_entry.get(), 'username')):
            self.page.flabel.config(text="Username already taken.\nPlease enter a unique username.")
            return

        if(self.page.email_entry.get() == "" or self.page.email_entry.get() == "Enter Your E-Mail"):
            self.page.flabel.config(text="Please enter an e-mail.")
            return

        if(userDB.check_valid_email(self.page.email_entry.get()) == False):
            self.page.flabel.config(text="Invalid e-mail format. Verify your input.")
            return

        if(userDB.check_valid_email(self.page.email_entry.get()) == None):
            self.page.flabel.config(text="E-mail already registered. Forgot your\nusername or password? Try the 'Forgot\nusername/password' button on the login page!")
            return

        if(self.page.Pass_entry.get() == "" or 
           self.page.Pass_reentry.get() == "" or
           self.page.Pass_entry.get() == "Choose a Password" or
           self.page.Pass_reentry.get() == "Re-Enter Password"):
            self.page.flabel.config(text="Please do not leave the\npassword fields blank.")
            return

        if(userDB.check_valid_password(self.page.Pass_entry.get()) == 0):
            self.page.flabel.config(text="Password must be at least 7 characters!")
            return

        elif(userDB.check_valid_password(self.page.Pass_entry.get()) == 1):
            self.page.flabel.config(text="Password must contain at least (1) digit.")
            return

        elif(userDB.check_valid_password(self.page.Pass_entry.get()) == 2):
            self.page.flabel.config(text="Password must contain at least (1)\nuppercase character")
            return

        elif(userDB.check_valid_password(self.page.Pass_entry.get()) == 3):
            self.page.flabel.config(text="Password must contain at least (1)\nspecial character(!#$%&'()*+,-./[\\\]^_`{|}~)")
            return

        if(self.page.Pass_entry.get() != self.page.Pass_reentry.get()):
            self.page.flabel.config(text="Passwords do not match!")
            return

        elif(userDB.register_user(self.page.Name_entry.get(), self.page.Pass_entry.get(), self.page.email_entry.get())  == True):
            self.page.flabel.config(text="")
            self.switch_page(LoginPage)
            return

        elif(userDB.register_user(self.page.Name_entry.get(), self.page.Pass_entry.get(), self.page.email_entry.get()) == False):
            self.page.flabel.config(text="User already registered. \nPlease log in using your credentials")
            return

    def forgotUser(self): # goes to forgot user page
        self.switch_page(FRegistrationPage)

    def retrieveUserInfo(self):
        valid_email = userDB.check_valid_email(self.page.email_entry.get())

        if(valid_email == False):
            self.page.mlabel.config(text="Invalid E-Mail format!\nPlease check your entry.", foreground="red")
            return

        else:
            tempUser = userDB.forgot_user_info(self.page.email_entry.get())
            self.newpass = ""

            if(tempUser is not None):
                full_username_label = "Username: " + str(tempUser.name)
                self.page.usernamelabel.config(text=full_username_label)

                if(self.page.Pass_entry.get() == "" or 
                   self.page.Pass_reentry.get() == "" or
                   self.page.Pass_entry.get() == "Choose a Password" or
                   self.page.Pass_reentry.get() == "Re-Enter Password"):
                    self.page.mlabel.config(text="Please do not leave the\npassword fields blank.")
                    return

                if(userDB.check_valid_password(self.page.Pass_entry.get()) == 0):
                    self.page.mlabel.config(text="Password must be at least 7 characters!")
                    return

                elif(userDB.check_valid_password(self.page.Pass_entry.get()) == 1):
                    self.page.mlabel.config(text="Password must contain at least (1) digit.")
                    return

                elif(userDB.check_valid_password(self.page.Pass_entry.get()) == 2):
                    self.page.mlabel.config(text="Password must contain at least (1)\nuppercase character")
                    return

                elif(userDB.check_valid_password(self.page.Pass_entry.get()) == 3):
                    self.page.mlabel.config(text="Password must contain at least (1)\nspecial character(!#$%&'()*+,-./[\\\]^_`{|}~)")
                    return

                if(self.page.Pass_entry.get() != self.page.Pass_reentry.get()):
                    self.page.mlabel.config(text="Passwords do not match!")
                    return

                self.newpass = self.page.Pass_entry.get()
                userDB.update_user_info(self.newpass, 'password', tempUser.id)
                self.page.mlabel.config(text="User information changed successfully", foreground="green")
                return

            else:
                self.page.usernamelabel.config(text="")
                self.page.mlabel.config(text="E-mail not currently registered!")
                return

    def returnLogIn(self): # Returns to the Log In page.
        self.switch_page(LoginPage)

    def send(self): # The send message button on Main Page.
        if((self.page.inputField.get() != "Click here to type") and 
           (self.page.inputField.get() != "")):
            #call sendMsg here
            self.page.msgList.configure(state=NORMAL)
            Client.sendMsg(self, self, self.currentUser,)
            self.page.msgList.configure(state=DISABLED)
            self.page.inputField.delete(0, "end")
            self.page.inputField.insert(0, "")
    
    def sendEnter(self, event): # Event that sends the message if Enter is pressed.
        if((self.page.inputField.get() != "Click here to type") and
           (self.page.inputField.get() != "")):
            self.page.msgList.configure(state=NORMAL)
            Client.sendMsg(self, self, self.currentUser,)
            self.page.msgList.configure(state=DISABLED)
            self.page.inputField.delete(0, "end")
            self.page.inputField.insert(0, "")

    def ChangeGroupChat(self, group_id=None, by_groupName = False, updateName = False, login = False):
        if(updateName == False):
            self.page.msgList.configure(state=NORMAL)
            self.page.msgList.delete("1.0", "end")
            self.page.msgList.configure(state=DISABLED)

        if(login == True):
            print("Logging in user...")
            self.currentGroup = userDB.load_group_info(group_id)
            Client.loginUser(self, self, self.currentUser, self.currentGroup.id)
            self.page.groupLabel.config( text="Current Group Chat: "+ self.currentGroup.name)
            print("Done log in")
        elif(group_id != None and group_id != ""):
            self.currentGroup = userDB.load_group_info(group_id)
            Client.changeGroup(self, self, self.currentUser, self.currentGroup.id)
            self.page.groupLabel.config( text="Current Group Chat: "+ self.currentGroup.name)
        # Change group chats, only if the selected group is different from the current.
        elif self.page.groupListBox.get(ACTIVE) != self.currentGroup.name:
            self.currentGroup = userDB.load_group_info(None, self.page.groupListBox.get(ACTIVE), self.currentUser.id, 'group_name')
            Client.changeGroup(self, self, self.currentUser, self.currentGroup.id,)
            self.page.groupLabel.config( text="Current Group Chat: "+ self.currentGroup.name)
        elif(group_id == ""):
            self.currentGroup = userDB.load_group_info('00000000')
            Client.changeGroup(self, self, self.currentUser, self.currentGroup.id)
            self.page.groupLabel.config( text="Current Group Chat: "+self.currentGroup.name)

    def ChangeFriendChat(self, friend_id=None):
        # Change group chats, only if the selected group is different from the current.
        print("Friend ID: %s" % friend_id)

        if self.page.friendListBox.get(ACTIVE) != self.currentGroup.name:
            print("clicked" + self.page.friendListBox.get(ACTIVE))
            self.page.msgList.configure(state=NORMAL)
            self.page.msgList.delete("1.0", "end")
            self.page.msgList.configure(state=DISABLED)
            self.currentGroup = userDB.load_group_info(None, self.page.friendListBox.get(ACTIVE), self.currentUser.id, 'friend_chat')
            print("THIS IS YOUR ID: %s" % self.currentGroup.id)

            Client.changeGroup(self, self, self.currentUser, self.currentGroup.id,)
            self.page.groupLabel.config( text="Direct Chat Room: "+ self.currentGroup.name)

    def insertNewGroup(self, CreateGroupPopup):
        newName = self.createGroupOpen.new_group_name.get()

        if(newName == ""):
            self.createGroupOpen.glabel.config(text="Please enter a group name!", foreground= "red")
            return
        
        else:
            group_id = userDB.create_group_id()
            userDB.join_group(group_id, newName, self.currentUser.id)
            self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')
            self.createGroupOpen.glabel.config(text=("Created Group! ID: " +str(group_id)), foreground= "yellow")
            self.page.updateGroupList(self.currentUser.groups)

    def joinNewGroup(self, JoinGroupPopup):
        groupID = self.joinGroupOpen.join_group_id.get()

        if(groupID not in self.currentUser.groups):
            if(userDB.checkGroupExistence(groupID) == True):
                groupName = userDB.get_group_name(groupID)
                userDB.join_group(groupID, groupName, self.currentUser.id)
                self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')
                self.joinGroupOpen.jlabel.config(text="Joined Group!", foreground= "yellow")
                self.page.updateGroupList(self.currentUser.groups)
            else:
                self.joinGroupOpen.jlabel.config(text="Group does not exist!", foreground = "red")

        else:
            self.joinGroupOpen.jlabel.config(text="Already in this group!", foreground = "red")

    def leaveCurrentGroup(self):
        if(self.currentGroup.id == '00000000'):
            print("You cannot leave General group!")
            return
        else:
            print("Leaving current group...")
            userDB.leave_group(self.currentGroup.id, self.currentUser.id)
            self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')
            self.page.updateGroupList(self.currentUser.groups)
            self.currentGroup = userDB.load_group_info('00000000')
            self.ChangeGroupChat(self.currentGroup.id)

    def changeGroupInfo(self, GroupSettingsPopup):
        if(self.currentGroup.id == '00000000'):
            GroupSettingsPopup.errLabel.config(text="You cannot modify the general group!", foreground= "red")
            return
        elif(GroupSettingsPopup.changeGroupNameInput.get() != "" ):
            userDB.update_group_info(GroupSettingsPopup.changeGroupNameInput.get(), 'group_name', self.currentGroup.id)
            self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')
            self.currentGroup = userDB.load_group_info(self.currentGroup.id)
            self.page.updateGroupList(self.currentUser.groups)
            self.ChangeGroupChat(self.currentGroup.id, updateName = True)

            ## UPDATE THE LISTS OF ALL LOGGED IN USERS IN THE LIST
            Client.updateAllGroupMembers(self, self, self.currentGroup.member_ids)

        else:
            GroupSettingsPopup.errLabel.config(text="Please enter a new group name!", foreground="red")

    def updateAllLists(self):
        self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')
        self.currentGroup = userDB.load_group_info(self.currentGroup.id)
        self.page.initGroupList(self.currentUser.groups)
        self.page.initFriendList(self.currentUser)
        self.page.updateGroupList(self.currentUser.groups)
        self.page.updateFriendList(self.currentUser)
        self.ChangeGroupChat(self.currentGroup.id, updateName = True)

    def addFriend(self, AddFriendPopup):
        newFriend = User()

        newFriend.name = self.addFriendOpen.new_friend_name.get()

        if(newFriend.id not in self.currentUser.friends):
            if(userDB.checkAccExistence(newFriend.name, 'username') and newFriend.name != self.currentUser.name): #if the account is found, add
                # append to user friends list
                newFriend = userDB.load_user_info(newFriend.name)
                groupID = userDB.create_group_id()

                print("Friend chat ID: %s" % groupID)

                userDB.join_group(groupID, newFriend.name, self.currentUser.id, 'dm')
                userDB.join_group(groupID, self.currentUser.name, newFriend.id, 'dm')
            
                self.currentUser = userDB.load_user_info(None, self.currentUser.id, 'user_id')
                print("My friends!!!!!!!!!!!!!!!!!!")
                print(self.currentUser.friends)
                AddFriendPopup.friendlabel.config(text="User found!", foreground="yellow")
                self.page.updateFriendList(self.currentUser)

                ## UPDATE NEW FRIEND'S LIST IF THEY ARE LOGGED ON
                Client.updateAllGroupMembers(self, self, self.currentGroup.member_ids)
            else:
                AddFriendPopup.friendlabel.config(text="User not found!", foreground="red")
        else:
            AddFriendPopup.friendlabel.config(text="Friend already added!", foreground="red")

#Initialize class call and set window size of login window
app = Controller()
app.geometry("230x250")
path = os.path.dirname(os.path.abspath(__file__))
img = PhotoImage(file=os.path.join(path, 'knk_icon.gif'))
app.tk.call('wm', 'iconphoto', app._w, img)
app.resizable(width=False, height=False)
app.mainloop()