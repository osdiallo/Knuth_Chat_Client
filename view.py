# View class to read input fromuser and output a U
from tkinter import *
from userDB import User
from userDB import load_group_info
from userDB import Group
from tkinter import _setit
from tkinter import ttk
import os


# Initialize the frame (tkinter class) to be the view window
class LoginPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        self.Name_entry = None
        self.Pass_entry = None
        self.elabel = None
        self.init_view(parent, controller)

    def hide(self):
        self.pack_forget()
    
    # This initializes the view; where buttons/boxes go
    def init_view(self, parent, controller):
        bkc = "SeaGreen3"

        self.config(background=bkc)
        #controller.title("Login Page")

        #self.frame.
        label = Label(self, text="Knuth Konnections", bg=bkc)
        label.config(width=0, font=("TkDefaultFont", 15))
        #label.grid(columnspan=2, pady=(10,0))
        label.pack()

        #Username Entry
        self.Name_entry = Entry(self)
        self.Name_entry.insert(0, "Username")
        self.Name_entry.bind("<FocusIn>", controller.click)
        self.Name_entry.bind("<FocusOut>", controller.clickout)
        self.Name_entry.config(fg = 'grey')

        #Password Entry
        self.Pass_entry = Entry(self)
        self.Pass_entry.insert(0, "Password")
        self.Pass_entry.bind("<Return>", controller.enterP)
        self.Pass_entry.bind("<FocusIn>", controller.clickP)
        self.Pass_entry.bind("<FocusOut>", controller.clickoutP)
        self.Pass_entry.config(fg = 'grey')

        self.Name_entry.pack(pady=5)
        self.Pass_entry.pack(pady=5)

        self.rememberUser = IntVar()
        self.rememberUser.set(0)
        self.rememberMe = Checkbutton(self, text="Remember me", variable=self.rememberUser, onvalue=1, offvalue=0, bg=bkc)
        self.rememberMe.pack()

        self.sin = Button(self, text="Sign In", bg="SlateGray2", command=controller.logInClick)
        self.sin.pack()

        self.elabel = Label(self, text="", bg=bkc)
        self.elabel.config(width=200, font=("TkDefaultFont", 10), foreground="red")
        self.elabel.pack()

        self.sup = Label(self, text="New User? Sign up Today!", bg=bkc)
        self.sup.pack()

        self.nus = Button(self, text="Sign Up", bg="SlateGray2", command=controller.registerClick)
        self.nus.pack()

        self.fUserInfo = Button(self, text="Forgot username/password", bg="SlateGray2", command=controller.forgotUser)
        self.fUserInfo.pack(pady=5)

class RegistrationPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.Name_entry = None
        self.email_entry = None
        self.Pass_entry = None
        self.Pass_reentry = None
        self.flabel = None

        self.init_view(controller)

    # This initializes the view; where buttons/boxes go
    def init_view(self, controller):
        bkc = "SeaGreen3"

        self.config(background=bkc)
        title = Label(self, text="User Registration", bg=bkc)
        title.config(width=0, font=("TkDefaultFont", 15))
        title.pack()

        self.Name_entry = Entry(self)
        self.Name_entry.insert(0, "Create a Username")
        self.Name_entry.bind("<FocusIn>", controller.clickCU)
        self.Name_entry.bind("<FocusOut>", controller.clickoutCU)
        self.Name_entry.config(fg = 'grey')

        self.email_entry = Entry(self)
        self.email_entry.insert(0, "Enter Your E-Mail")
        self.email_entry.bind("<FocusIn>", controller.clickCE)
        self.email_entry.bind("<FocusOut>", controller.clickoutCE)
        self.email_entry.config(fg = 'grey')

        self.Pass_entry = Entry(self)
        self.Pass_entry.insert(0, "Choose a Password")
        self.Pass_entry.bind("<FocusIn>", controller.clickCP)
        self.Pass_entry.bind("<FocusOut>", controller.clickoutCP)
        self.Pass_entry.config(fg = 'grey')

        self.Pass_reentry = Entry(self)
        self.Pass_reentry.insert(0, "Re-Enter Password")
        self.Pass_reentry.bind("<FocusIn>", controller.clickCRP)
        self.Pass_reentry.bind("<FocusOut>", controller.clickoutCRP)
        self.Pass_reentry.config(fg = 'grey')

        self.Name_entry.pack(pady=5)
        self.email_entry.pack(pady=5)
        self.Pass_entry.pack(pady=5)
        self.Pass_reentry.pack(pady=5)

        self.flabel = Label(self, text="", bg=bkc)
        self.flabel.config(width=200, font=("TkDefaultFont", 10), foreground="red")
        self.flabel.pack()

        cReg = Button(self, text="Complete Registration", bg="SlateGray2", command=controller.completeRegClick)
        cReg.pack()

        backToLogIn = Button(self, text="Return to Log In Page", bg="SlateGray2", command=controller.returnLogIn)
        backToLogIn.pack(pady=(10,0))

class FRegistrationPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.email_entry = None
        self.usernamelabel = None
        self.init_view(controller)

    # This initializes the view; where buttons/boxes go
    def init_view(self, controller):
        bkc = "SeaGreen3"

        self.config(background=bkc)
        title = Label(self, text="Forgot username/password", bg=bkc)
        title.config(width=0, font=("TkDefaultFont", 13))
        title.pack()

        self.usernamelabel = Label(self, text="", bg=bkc)
        self.usernamelabel.config(width=200, font=("TkDefaultFont", 10), foreground="black")
        self.usernamelabel.pack()

        self.email_entry = Entry(self)
        self.email_entry.insert(0, "Enter your email")
        self.email_entry.bind("<FocusIn>", controller.clickFE)
        self.email_entry.bind("<FocusOut>", controller.clickoutFE)
        self.email_entry.config(fg = 'grey')

        self.Pass_entry = Entry(self)
        self.Pass_entry.insert(0, "Choose a Password")
        self.Pass_entry.bind("<FocusIn>", controller.clickCP)
        self.Pass_entry.bind("<FocusOut>", controller.clickoutCP)
        self.Pass_entry.config(fg = 'grey')

        self.Pass_reentry = Entry(self)
        self.Pass_reentry.insert(0, "Re-Enter Password")
        self.Pass_reentry.bind("<FocusIn>", controller.clickCRP)
        self.Pass_reentry.bind("<FocusOut>", controller.clickoutCRP)
        self.Pass_reentry.config(fg = 'grey')

        self.email_entry.pack(pady=5)
        self.Pass_entry.pack(pady=5)
        self.Pass_reentry.pack(pady=5)

        self.mlabel = Label(self, text="", bg=bkc)
        self.mlabel.config(width=200, font=("TkDefaultFont", 10), foreground="red")
        self.mlabel.pack()

        cReg = Button(self, text="Update user information", bg="SlateGray2", command=controller.retrieveUserInfo)
        cReg.pack()

        backToLogIn = Button(self, text="Return to Log In Page", bg="SlateGray2", command=controller.returnLogIn)
        backToLogIn.pack(pady=(10,0))

class ChatPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        new_style = ttk.Style()
        new_style.theme_create( "new_style", parent="alt", settings={
            "TNotebook": {
                "configure": { "tabmargins": [5, 0, 5, 5] }
               },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [13, 13],
                    "sticky": W+E
                    },}})
        #new_style.theme_use("new_style")

        self.update()
        self.groupList = []
        self.controller = controller
        self.init_view(controller)
        
    def init_view(self, controller):
        bkc = controller.realColor
        self.config(background=bkc)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ### FRAME INIT ###
        self.settingsFrame = Frame(self, background = bkc, width=500, height=100, padx=3, pady=2)
        self.groupNameFrame = Frame(self, background=bkc, width=500, height=10, padx=1, pady=2)
        self.inputFrame = Frame(self, bg=bkc, width=500, padx=1, pady=2)
        self.messages = Frame(self, bg=bkc, width=500, height=300, padx=1, pady=2)
        self.groups = Frame(self, background=bkc, width=500, padx=1, pady=2)
        self.groupListFrame = Frame(self, background = bkc, width=120, height=450)

        self.settingsFrame.grid(row=0, column=1, columnspan=5, sticky=N+E+W)
        self.groupListFrame.grid(row=0, column=0, rowspan=5, columnspan=2, sticky=W+N+S)
        self.groupNameFrame.grid(row=1, column=1, columnspan=5,sticky=N+W+E)
        self.messages.grid(row=2, column=1, columnspan=5,sticky=N+W+E)
        self.inputFrame.grid(row=3, column=1,columnspan=5,sticky=N+W+E+S)
        self.groups.grid(row=4, column=1,columnspan=5,sticky=W+E+N)

        ### FRAME 1 : Options Bar ###
        self.accSettingsButton = Button(self.settingsFrame, bg="SlateGray2", text = "Acc Settings", command = controller.accSettingsButtonClick)
        self.groupSettingsButton = Button(self.settingsFrame, bg="SlateGray2", text = "Group Settings", command = controller.groupSettingsButtonClick)
        self.knuthKonnectionsLabel = Label(self.settingsFrame, bg="SeaGreen3", text="Knuth Konnections", font=("Helvetica, 14"))
        self.logOutButton = Button(self.settingsFrame, bg="SlateGray2", text = "Log Out", command = controller.logOutClick)
        self.groupListLabel = Label(self.settingsFrame, bg=bkc, text="Group List", font=("Helvetica, 12"))

        #self.groupListLabel.grid(row=0, column=0, padx=(35, 50), sticky=W)
        self.logOutButton.grid(row=0, column=6, padx=3)
        self.accSettingsButton.grid(row=0, column=5, sticky=E)
        self.knuthKonnectionsLabel.grid(row=0, column=3,columnspan=2,padx=20, sticky=E)
        self.groupSettingsButton.grid(row=0, column=2,sticky=E)

        ## FRAME 2 : Titles###
        self.groupNameFrame.columnconfigure(2, weight=1)

        self.groupLabel = Label(self.groupNameFrame, width=50, background="SlateGray2", text="Current Group Chat: "+str(controller.currentGroup.name), font='Helvetica 10 bold')
        
        self.groupLabel.grid(row=1, column=1, columnspan=2, sticky=N+W+E)

        ## FRAME 3: Chat Window ###
        self.messages.rowconfigure(0, weight=4)

        self.inputMsg = StringVar()
        self.inputMsg.set("Click here to type")
        self.scrollbar = Scrollbar(self.messages, orient="vertical")

        self.msgList = Text(self.messages, wrap=WORD, height=24, width=53, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.msgList.yview)
        self.msgList.configure(state=DISABLED)

        self.msgList.grid(row=0, column=0, columnspan=4, sticky=N+W+E)
        self.scrollbar.grid(row=0, column=4, sticky=N+S)

        ### FRAME 4: Input Field ###
        self.inputFrame.columnconfigure(0, weight=4)
        self.inputFrame.columnconfigure(4, weight=1)

        self.inputField = Entry(self.inputFrame, textvariable=self.inputMsg)
        self.inputField.bind("<Return>", controller.sendEnter)
        self.inputField.bind("<FocusIn>", controller.clickIF)
        self.inputField.bind("<FocusOut>", controller.clickoutIF)
        self.inputField.config(fg="grey", width=60)

        self.sendButton = Button(self.inputFrame, text="Send", bg="SlateGray2", command=controller.send)
        
        self.inputField.grid(row=3, column=0, columnspan=3, sticky=W+N+S+E)
        self.sendButton.grid(row=3, column=4, sticky=E+W)

        ### FRAME 5: Group Options ###
        self.currentGroupTitle = StringVar()
        self.currentGroupTitle.set("General")
        
        #self.createGroupButton = Button(self.groups, bg='SlateGray2', text="Create Group", command=controller.createNewGroupClick)
        #self.joinGroupButton = Button(self.groups, bg='SlateGray2', text="Join Group", command=controller.joinNewGroupClick)
        self.leaveCurrentGroup = Button(self.groups, bg='SlateGray2', text="Leave Group", command = controller.leaveCurrentGroup)

        #self.createGroupButton.grid(row=5, column=0, padx=(75,0), sticky=W+E)
        #self.joinGroupButton.grid(row=5, column=1, padx=(25,20),sticky=W+E)
        self.leaveCurrentGroup.grid(row=5, column=2, padx=(5,95), sticky=W+E)
        
        ### FRAME 6 GROUP LIST ###
        self.FriendsListBox = ttk.Notebook(self.groupListFrame, height=485, width=135)

        self.userGroupListFrame = ttk.Frame(self.FriendsListBox)
        self.userFriendsListFrame = ttk.Frame(self.FriendsListBox)

        self.groupListBox = Listbox(self.userGroupListFrame, height=24, width=19)
        self.groupButton = Button(self.userGroupListFrame, bg="SlateGray2", text="Change Group Chat", command=controller.ChangeGroupChat)       
        self.createGroupButton = Button(self.userGroupListFrame, bg='SlateGray2', text="Create Group", command=controller.createNewGroupClick)
        self.joinGroupButton = Button(self.userGroupListFrame, bg='SlateGray2', text="Join Group", command=controller.joinNewGroupClick)

        self.friendListBox = Listbox(self.userFriendsListFrame, height=26, width=19)
        self.addFriendButton = Button(self.userFriendsListFrame, bg="SlateGray2", text="Add Friend", command=controller.addNewFriend)   
        self.dmFriendButton = Button(self.userFriendsListFrame, bg="SlateGray2", text="Message Friend", command=controller.ChangeFriendChat)

        self.FriendsListBox.add(self.userGroupListFrame, text="Groups")
        self.FriendsListBox.add(self.userFriendsListFrame, text="Friends")

        self.FriendsListBox.grid(row=0, column=0, rowspan=5, columnspan=2, sticky='NESW', padx=10)
        
        self.groupListBox.grid(row=0, column=0, sticky=N+W, padx=10)
        self.groupButton.grid(row=1, column=0, sticky=S+W+E, padx=10, pady=2)
        self.createGroupButton.grid(row=2, column=0, sticky=S+W+E, padx=10, pady=2)
        self.joinGroupButton.grid(row=3, column=0, sticky=S+W+E, padx=10, pady=2)

        self.friendListBox.grid(row=0, column=0, sticky=N+W, padx=10)
        self.addFriendButton.grid(row=1, column=0, sticky=S+W+E, padx=10, pady=2)
        self.dmFriendButton.grid(row=2, column=0, sticky=S+W+E, padx=10, pady=2)

    def initGroupList(self, group_list):
        self.groupsIDConverted = []
        self.groupListBox = Listbox(self.userGroupListFrame, height=24, width=19)

        if(len(group_list) > 0):
            for group in group_list:
                groupInfo = load_group_info(group[0])
                self.groupsIDConverted.append(groupInfo.name)

            for group in self.groupsIDConverted:
                self.groupListBox.insert(END, group)
        
        self.groupListBox.grid(row=0, column=0, sticky=N+W, padx=10)

    def initFriendList(self, currentUser):
        friend_list = currentUser.friends
        self.friendListBox = Listbox(self.userFriendsListFrame, height=26, width=19)

        if(len(friend_list) > 0):
            for friend in friend_list:
                #print("This is your friend %s: " % friend[0])
                friendGroupInfo = load_group_info(None, friend[0], currentUser.id, 'friend_chat')
                #print(friendGroupInfo.name)
                self.friendListBox.insert(END, friendGroupInfo.name)
        
        self.friendListBox.grid(row=0, column=0, sticky=N+W, padx=10)

    def updateGroupList(self, group_list):
        self.groupList = []
        self.groupListBox.delete(0, END)

        for group in group_list:
            groupInfo = load_group_info(group[0])
            self.groupList.append(groupInfo.name)
            self.groupListBox.insert(END, groupInfo.name)

    def updateFriendList(self, currentUser):
        self.friendList = []
        self.friendListBox.delete(0, END)
        #print("Update FriendList")

        for friend in currentUser.friends:
            #print(friend)
            friendGroupInfo = load_group_info(None, friend[0], currentUser.id, 'friend_chat')
            self.friendList.append(friendGroupInfo.name)
            self.friendListBox.insert(END, friendGroupInfo.name)

class AccSettingsPopup(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.controller.accSettingsOpen = self
        self.userNameChangeInput = StringVar()
        self.emailChangeInput = StringVar()
        self.passwordChangeInput = StringVar()
        self.confirmChangeInput = StringVar()
        self.oldPasswordInput = StringVar()

        bkc = controller.realColor
        self.window = Toplevel()

        #Icon at top of window
        path = os.path.dirname(os.path.abspath(__file__))
        img = PhotoImage(file=os.path.join(path, 'knk_icon.gif'))
        self.window.tk.call('wm', 'iconphoto', self.window._w, img)
        
        self.window.config(background=bkc)
        self.window.resizable(width=False, height=False)
        self.window.protocol("WM_DELETE_WINDOW", self.destroyPopup)
        self.window.wm_geometry("280x355")
        self.window.wm_title("Account Settings")

        self.window.config(background=bkc)
        positionRight = int(self.controller.winfo_screenwidth()/2 - 140)
        positionDown = int(self.controller.winfo_screenheight()/3 - 145)
        self.window.wm_geometry("280x355+{}+{}".format(positionRight, positionDown))

        self.title = Label(self.window, background=bkc, font=("TkDefaultFont", 12), text="Change Account Settings")
        self.title.grid(row=0,columnspan=2, pady=5, padx=(10,0))
        self.title.config(bg = bkc, font='bold')

        ##start Old pass entry
        self.oldPassLabel = Label(self.window, background=bkc, text="Enter Password")
        self.oldPassLabel.grid(row=1, column=0, pady=(2,7), padx=5)
        self.oldPassLabel.config(background=bkc)

        self.oldPassEntry = Entry(self.window, textvariable=self.oldPasswordInput)
        self.oldPassEntry.config(fg = "black", show="*")
        self.oldPassEntry.grid(row=1, column=1,pady=(2,7))

        ##start UserName (ChatName) change
        self.userInstruction = Label(self.window, background=bkc, text="Change Username")
        self.userInstruction.grid(row=2, column=0,pady=(2,7),padx=5)
        self.userInstruction.config(background=bkc)

        self.changeUserNameInput = Entry(self.window, textvariable=self.userNameChangeInput)
        self.changeUserNameInput.grid(row=2, column=1,pady=(2,7))

        ##start email change
        self.emailInstruction = Label(self.window, background=bkc, text="Change E-Mail")
        self.emailInstruction.grid(row=3, column=0,pady=(2,7),padx=5)
        self.emailInstruction.config(background=bkc)

        self.changeEmailInput = Entry(self.window, textvariable=self.emailChangeInput)
        self.changeEmailInput.grid(row=3, column=1,pady=(2,7))

        ##start Password change
        self.passInstruction = Label(self.window, background=bkc, text="Change Password")
        self.passInstruction.grid(row=4, column=0,pady=(2,7),padx=5)
        self.passInstruction.config(background=bkc)

        self.changePasswordInput = Entry(self.window, textvariable=self.passwordChangeInput)
        self.changePasswordInput.config(fg = "black", show="*")
        self.changePasswordInput.grid(row=4, column=1,pady=(2,7))

        ##start Confirm Password change
        self.confirmInstruction = Label(self.window, background=bkc, text="Re-enter New Password")
        self.confirmInstruction.grid(row=5, column=0,pady=(2,7),padx=5)
        self.confirmInstruction.config(background=bkc)

        self.confirmPasswordInput = Entry(self.window, textvariable=self.confirmChangeInput)
        self.confirmPasswordInput.config(fg = "black", show="*")
        self.confirmPasswordInput.grid(row=5, column=1,pady=(2,7))

        ##start Theme change
        self.themeInstruction = Label(self.window, background = bkc, text="Choose Theme")
        self.themeInstruction.grid(row=6, column=0, pady=(2,7), padx=5)
        self.themeInstruction.config(background=bkc)

        self.options = ["Green", "Blue", "Red", "Orange"]
        self.defaultVal = StringVar()
        self.defaultVal.set(self.options[0])

        self.themeDropDown = OptionMenu(self.window, self.defaultVal, *self.options, command= lambda X: controller.changeTheme(self))
        self.themeDropDown.config(bg = "SlateGray2", highlightbackground = bkc)
        self.themeDropDown["menu"].config(bg="SlateGray2")
        self.themeDropDown.grid(row=6, column=1, pady=(2,7))

        ##start BackgroundText change
        self.textInstruction = Label(self.window, background = bkc, text="Choose Text Background")
        self.textInstruction.grid(row=7, column=0, pady=(2,7), padx=5)
        self.textInstruction.config(background=bkc)

        self.opt = ["Lime", "Salmon", "Gold", "Cyan", "Dark Orchid", "Hot pink", "Gainsboro"]
        self.defaultV = StringVar()
        self.defaultV.set(self.opt[0])

        self.theDropDown = OptionMenu(self.window, self.defaultV, *self.opt, command= lambda X: controller.Textbg(self))
        self.theDropDown.config(bg = "SlateGray2", highlightbackground = bkc)
        self.theDropDown["menu"].config(bg="SlateGray2")
        self.theDropDown.grid(row=7, column=1, pady=(2,7))

        ##start Submit button
        self.submitChanges = Button(self.window, bg="SlateGray2", text="Submit Changes", command= lambda: controller.changeUserAndPass(self))
        self.submitChanges.grid(row=8, columnspan=2, pady=(2,3), padx=(10,0))

        ##start Error label
        self.errLabel = Label(self.window, background=bkc, text="")
        self.errLabel.config(foreground="red")
        self.errLabel.config(background=bkc)
        self.errLabel.grid(row=9, columnspan=2, pady=2, padx=(10,0))

        self.exitAccSettings = Button(self.window, text="Exit", bg="SlateGray2", command=self.destroyPopup)
        self.exitAccSettings.grid(row=10, columnspan=2, pady=(2,3), padx=(10,0))

    def destroyPopup(self):
        self.controller.accSettingsOpen = None
        self.window.destroy()

class GroupSettingsPopup(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.controller.groupSettingsOpen = self
        self.groupNameChangeInput = StringVar()
        self.invitedUser = StringVar()

        bkc = controller.realColor
        self.window = Toplevel()

        #Icon at top of window
        path = os.path.dirname(os.path.abspath(__file__))
        img = PhotoImage(file=os.path.join(path, 'knk_icon.gif'))
        self.window.tk.call('wm', 'iconphoto', self.window._w, img)
        
        self.window.config(background=bkc)
        self.window.protocol("WM_DELETE_WINDOW", self.destroyPopup)
        self.window.wm_title("Group Settings")

        self.window.config(background=bkc)
        self.window.resizable(width=False, height=False)
        positionRight = int(self.controller.winfo_screenwidth()/2 - 140)
        positionDown = int(self.controller.winfo_screenheight()/3 - 135)
        self.window.wm_geometry("260x180+{}+{}".format(positionRight, positionDown))

        self.title = Label(self.window, background=bkc, font=("TkDefaultFont", 12), text="Change Group Settings")
        self.title.grid(row=0,columnspan=2, pady=5, padx=(10,0))
        self.title.config(bg = bkc, font='bold')

        ## START DISPLAY GROUP ID
        self.groupIDLabel = Label(self.window, background=bkc, text="Group ID: ")
        self.groupIDLabel.grid(row=1, column=0)

        self.groupID = Label(self.window, background=bkc, text=str(controller.currentGroup.id))
        self.groupID.grid(row=1, column=1)

        ## START CHANGE GROUP NAME
        self.groupInstruction = Label(self.window, background=bkc, text="Change Group name")
        self.groupInstruction.grid(row=2, column=0, pady=(2,7), padx=5)
        self.groupInstruction.config(background=bkc)

        self.changeGroupNameInput = Entry(self.window, textvariable=self.groupNameChangeInput)
        self.changeGroupNameInput.grid(row=2, column=1,pady=(2,7))

        ## START INVITE USER

        ##start Error label
        self.errLabel = Label(self.window, background=bkc, text="")
        self.errLabel.config(foreground="red")
        self.errLabel.config(background=bkc)
        self.errLabel.grid(row=3, columnspan=2, pady=2, padx=(10,0))

        ##start Submit button
        self.submitChanges = Button(self.window, bg="SlateGray2", width=13, text="Submit Changes", command= lambda : controller.changeGroupInfo(self))
        self.submitChanges.grid(row=4, columnspan=2, pady=3)

        self.exitGroupSettings = Button(self.window, text="Exit", width=13, bg="SlateGray2", command=self.destroyPopup)
        self.exitGroupSettings.grid(row=5, columnspan=2, pady=3)

    def destroyPopup(self):
        self.controller.groupSettingsOpen = None
        self.window.destroy()

class CreateGroupPopup(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controller.createGroupOpen = self
        self.new_group_name = None
        self.groupNameInput = StringVar()
        self.init_view(parent, controller)

    def init_view(self, parent, controller):
        bkc = controller.realColor
        self.window = Toplevel()
        
        #Icon at top of window
        path = os.path.dirname(os.path.abspath(__file__))
        img = PhotoImage(file=os.path.join(path, 'knk_icon.gif'))
        self.window.tk.call('wm', 'iconphoto', self.window._w, img)

        self.window.config(background=bkc)
        self.window.protocol("WM_DELETE_WINDOW", self.destroyPopup)
        self.window.wm_title("Create Group Settings")

        self.window.config(background=bkc)
        self.window.resizable(width=False, height=False)
        positionRight = int(self.controller.winfo_screenwidth()/2 - 140)
        positionDown = int(self.controller.winfo_screenheight()/3 - 135)
        self.window.wm_geometry("300x50+{}+{}".format(positionRight, positionDown))

        self.new_group_name = Entry(self.window, textvariable=self.groupNameInput)
        self.new_group_name.insert(0, "New Group Name")
        self.new_group_name.bind("<FocusIn>", controller.clickCGN)
        self.new_group_name.bind("<FocusOut>", controller.clickoutCGN)
        self.new_group_name.config(fg = 'grey')

        self.glabel = Label(self.window, text="", bg=bkc)
        self.glabel.config(font=("TkDefaultFont", 10), foreground="red")

        self.createGroup = Button(self.window, text="Create Group", bg="SlateGray2", command= lambda : controller.insertNewGroup(self))
        
        self.window.grid_columnconfigure(0, weight=3)
        self.window.grid_columnconfigure(3, weight=1)

        self.new_group_name.grid(row=0, column=0, sticky=W+E)
        self.glabel.grid(row=1, column=0, columnspan=4, sticky=W+E)
        self.createGroup.grid(row=0, column=3, sticky=W+E)

    def destroyPopup(self):
        self.controller.createGroupOpen = None
        self.window.destroy()

class JoinGroupPopup(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controller.joinGroupOpen = self
        self.join_group_id = StringVar()
        self.joinGroupInput = StringVar()
        self.init_view(parent, controller)

    def init_view(self, parent, controller):
        bkc = controller.realColor
        self.window = Toplevel()
        
        #Icon at top of window
        path = os.path.dirname(os.path.abspath(__file__))
        img = PhotoImage(file=os.path.join(path, 'knk_icon.gif'))
        self.window.tk.call('wm', 'iconphoto', self.window._w, img)
        
        self.window.config(background=bkc)
        self.window.resizable(width=False, height=False)
        self.window.protocol("WM_DELETE_WINDOW", self.destroyPopup)
        self.window.wm_title("Join New Group")

        self.window.config(background=bkc)
        positionRight = int(self.controller.winfo_screenwidth()/2 - 200)
        positionDown = int(self.controller.winfo_screenheight()/3 - 135)
        self.window.wm_geometry("300x50+{}+{}".format(positionRight, positionDown))

        self.join_group_id = Entry(self.window, textvariable=self.joinGroupInput)
        self.join_group_id.insert(0, "Enter Group ID")
        self.join_group_id.bind("<FocusIn>", controller.clickJGN)
        self.join_group_id.bind("<FocusOut>", controller.clickoutJGN)
        self.join_group_id.config(fg = 'grey')

        self.jlabel = Label(self.window, text="", bg=bkc)
        self.jlabel.config(font=("TkDefaultFont", 10), foreground="red")
        
        self.joinGroup = Button(self.window, text="Join Group", bg="SlateGray2", command= lambda : controller.joinNewGroup(self))

        self.window.grid_columnconfigure(0, weight=3)
        self.window.grid_columnconfigure(3, weight=1)

        self.join_group_id.grid(row=0, column=0, columnspan=3, sticky=W+E)
        self.jlabel.grid(row=1, column=0, columnspan=4, sticky=W+E)
        self.joinGroup.grid(row=0, column=3, sticky=W+E)

    def destroyPopup(self):
        self.controller.joinGroupOpen = None
        self.window.destroy()

class AddFriendPopup(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.controller.addFriendOpen = self
        self.new_friend_name = StringVar()
        self.friendNameInput = StringVar()
        self.init_view(parent, controller)

    def init_view(self, parent, controller):
        bkc = controller.realColor
        self.window = Toplevel()
        
        #Icon at top of window
        path = os.path.dirname(os.path.abspath(__file__))
        img = PhotoImage(file=os.path.join(path, 'knk_icon.gif'))
        self.window.tk.call('wm', 'iconphoto', self.window._w, img)
        
        self.window.config(background=bkc)
        self.window.resizable(width=False, height=False)
        self.window.protocol("WM_DELETE_WINDOW", self.destroyPopup)
        self.window.wm_title("Add New Friend")

        self.window.config(background=bkc)
        positionRight = int(self.controller.winfo_screenwidth()/2 - 200)
        positionDown = int(self.controller.winfo_screenheight()/3 - 135)
        self.window.wm_geometry("300x50+{}+{}".format(positionRight, positionDown))

        self.new_friend_name = Entry(self.window, textvariable=self.friendNameInput)
        self.new_friend_name.insert(0, "Search For User...")
        self.new_friend_name.bind("<FocusIn>", controller.clickNFN)
        self.new_friend_name.bind("<FocusOut>", controller.clickoutNFN)
        self.new_friend_name.config(fg = 'grey')

        self.friendlabel = Label(self.window, text="", bg=bkc)
        self.friendlabel.config(font=("TkDefaultFont", 10), foreground="red")
        
        self.addFriend = Button(self.window, text="Add Friend", bg="SlateGray2", command= lambda : controller.addFriend(self))

        self.window.grid_columnconfigure(0, weight=3)
        self.window.grid_columnconfigure(3, weight=1)

        self.new_friend_name.grid(row=0, column=0, columnspan=3, sticky=W+E)
        self.friendlabel.grid(row=1, column=0, columnspan=4, sticky=W+E)
        self.addFriend.grid(row=0, column=3, sticky=W+E)

    def destroyPopup(self):
        self.controller.joinGroupOpen = None
        self.window.destroy()
