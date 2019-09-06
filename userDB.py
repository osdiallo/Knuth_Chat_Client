import time
import sys
import bcrypt
import sqlite3
import os.path
import uuid
import re
import random
import string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "user_info.db")

# registers user given a username and a password.
# users are added to a sqlite database
class User:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.password = ""
        self.email = ""
        self.groups = []
        self.friends = []
        self.theme = ""
        self.textbg = "Lime"
        #self.status <---- Tells if a user is online, must be implemented later

class Group:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.member_ids = []
        self.member_names = []
        self.numActiveUsers = 0

        # TODO: implement number of active users

# Checks if a table exists in a database. Creates the table
# if not
def checkTableExists(dbconn, tableName):
    cursor = dbconn.cursor()

    if(tableName == 'users'):
        create_sql_table = """CREATE TABLE IF NOT EXISTS {} (
                                    user_id text PRIMARY KEY,
                                    username text UNIQUE,
                                    password text,
                                    email text,
                                    theme text,
                                    textbg text
                                );""".format(tableName)

    elif(tableName == 'groups'):
        create_sql_table = """CREATE TABLE IF NOT EXISTS {} (
                                    group_id text KEY,
                                    group_name text,
                                    member_id text,
                                    group_type text
                                );""".format(tableName)

    cursor.execute(create_sql_table)
    cursor.close()

# Checks if an account exists with a given username or email.
# Returns true if a matching account is found, false otherwise
def checkAccExistence(var_to_search, param_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    checkTableExists(conn, 'users')

    search_user = "SELECT * FROM users WHERE {}=?".format(param_name)

    c.execute(search_user , (var_to_search,))
    accountExists = c.fetchone()
    
    if(accountExists):
        conn.close()
        return True
    else:
        conn.close()
        return False

# Checks if a group exists. Returns true if so, false otherwise
def checkGroupExistence(group_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    checkTableExists(conn, 'groups')
    
    search_group = "SELECT * FROM groups WHERE group_id=?"

    c.execute(search_group, (group_id,))
    groupExists = c.fetchone()
    
    if(groupExists):
        conn.close()
        return True
    else:
        conn.close()
        return False

# inserts a user in a SQLite Database given a username, password,
# and email. Return true if the user is successfully registered,
# false otherwise. all users are added to the general group chat
# after they register
def register_user(r_user_name, r_user_pass, r_user_email):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    checkTableExists(conn, 'users')
    checkTableExists(conn, 'groups')
    encrypted_pass = encrypt_pass(r_user_pass)

    theme_color = "Green"
    textb = "Lime"
    
    if(checkAccExistence(r_user_name, 'username')):
        conn.close()
        return False
    else:
        user_id = str(uuid.uuid4())
        print("User successfully registered. Welcome!")
        c.execute("INSERT INTO users \
            VALUES (?, ?, ?, ?, ?, ?)", (user_id, r_user_name, encrypted_pass, r_user_email, theme_color, textb));
        c.execute("INSERT INTO groups \
            VALUES (?, ?, ?, ?)", ('00000000', 'General', user_id, 'group'));
        conn.commit()
        conn.close()
        return True

# retrieves an encrypted password from the user database
# given a username as a key. if the user is found, return
# the encrypted password; otherwise, return empty string
def retrieve_pass(user_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE username=?" , (user_name,))
    user_pass = c.fetchone()
    
    if(user_pass):
        conn.close()
        return user_pass[0]
    else:
        nil = ''
        conn.close()
        return nil
  
# attempts to load a user and provide helpful messages if 
# an error is encountered. 
# returns 0 if user is not in the user database
# returns 1 if user is found in database
# returns 2 if inputted password does not match stored password for user
def login_user(l_user_name, l_user_pass):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    checkTableExists(conn, 'users')

    stored_user_pass  = retrieve_pass(l_user_name)

    if(stored_user_pass != ''):
        if(check_pass(l_user_pass, stored_user_pass)):
            return 1

        else:
            return 2

    else:
        return 0

# returns a user object given a username
def load_user_info(user_name, user_id = None, param='username'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    currentUser = User()

    if(param == 'username'):        
        currentUser.name = user_name
    
        c.execute("SELECT password FROM users WHERE username=?" , (user_name,))
        currentUser.password = c.fetchone()[0]

        c.execute("SELECT theme FROM users WHERE username=?" , (user_name,))
        currentUser.theme = c.fetchone()[0]

        c.execute("SELECT textbg FROM users WHERE username=?" , (user_name,))
        currentUser.textbg = c.fetchone()[0]

        c.execute("SELECT user_id FROM users WHERE username=?" , (user_name,))
        currentUser.id = c.fetchone()[0]

        c.execute("SELECT email FROM users WHERE username=?" , (user_name,))
        currentUser.email = c.fetchone()[0]

        c.execute("SELECT group_id FROM groups WHERE member_id=? AND group_type=?" , (currentUser.id, 'group'))
        list_of_group_ids = c.fetchall()

        currentUser.groups = list_of_group_ids

        c.execute("SELECT member_id FROM groups WHERE group_name=? AND group_type=?" , (currentUser.name, 'dm'))
        currentUser.friends = c.fetchall()

    elif(param == 'user_id'):
        currentUser.id = user_id

        c.execute("SELECT password FROM users WHERE user_id=?" , (user_id,))
        currentUser.password = c.fetchone()[0]

        c.execute("SELECT theme FROM users WHERE user_id=?" , (user_id,))
        currentUser.theme = c.fetchone()[0]

        c.execute("SELECT textbg FROM users WHERE user_id=?" , (user_id,))
        currentUser.textbg = c.fetchone()[0]

        c.execute("SELECT username FROM users WHERE user_id=?" , (user_id,))
        currentUser.name = c.fetchone()[0]

        c.execute("SELECT email FROM users WHERE user_id=?" , (user_id,))
        currentUser.email = c.fetchone()[0]

        c.execute("SELECT group_id FROM groups WHERE member_id=? AND group_type=?" , (user_id, 'group',))
        currentUser.groups = c.fetchall()

        c.execute("SELECT member_id FROM groups WHERE group_name=? AND group_type=?" , (currentUser.name, 'dm',))
        currentUser.friends = c.fetchall()

    conn.close()
    return currentUser

# loads information about a group given a group_id, returns a group object
def load_group_info(group_id, group_name = None, user_id = None, param='group_id'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    groupInfo = Group()

    if(param == 'group_id'):
        groupInfo.id = group_id
        c.execute("SELECT group_name FROM groups WHERE group_id=?" , (group_id,))
        groupInfo.name = c.fetchone()[0]

        c.execute("SELECT member_id FROM groups WHERE group_id=? AND group_type=?" , (group_id, 'group'))
        groupInfo.member_ids = c.fetchall()

    elif(param == 'group_name'):
        groupInfo.name = group_name

        c.execute("SELECT group_id FROM groups WHERE group_name=? AND member_id=?" , (groupInfo.name, user_id,))
        groupInfo.id = c.fetchone()[0]

        c.execute("SELECT member_id FROM groups WHERE group_id=? AND group_type=?" , (groupInfo.id, 'group'))
        groupInfo.member_ids = c.fetchall()
    
    elif(param == 'friend_chat'):
        if(len(group_name) < 30):
            friendObj = load_user_info(group_name)
        else:
            friendObj = load_user_info(None, group_name, 'user_id')

        #c.execute("SELECT group_name FROM groups WHERE group_type=? AND member_id=?" , ('dm', user_id,))
        groupInfo.name = friendObj.name

        groupInfo.member_ids.append(user_id)
        groupInfo.member_ids.append(friendObj.id)

        c.execute("SELECT group_id FROM groups WHERE group_type=? AND member_id=? AND group_name=?" , ('dm', user_id, friendObj.name))
        groupInfo.id = c.fetchone()[0]

    return groupInfo

# returns a user object given an email. returns None if the
# user is not found
def forgot_user_info(email):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    currentUser = User()
    currentUser.email = email

    if(checkAccExistence(email, 'email')):
        c.execute("SELECT password FROM users WHERE email=?" , (email,))
        currentUser.password = c.fetchone()[0]

        c.execute("SELECT username FROM users WHERE email=?" , (email,))
        currentUser.name = c.fetchone()[0]

        c.execute("SELECT user_id FROM users WHERE email=?" , (email,))
        currentUser.id = c.fetchone()[0]

        conn.close()
        return currentUser

    else:
        conn.close()
        return None

# verifies if the format of an email is appropriate, including extensions.
# checks first if email is already registered, returns none if so.
# Returns true if a given email is of the appropriate, false otherwise
def check_valid_email(email):
    if(not checkAccExistence(email, 'email')):
        if(re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            if(email[-3:] == "com" or email[-3:] == "edu" or email[-3:] == "gov"):
                return True
        return False
    return None

# checks validity of password. if the password does not meet certain requirements,
# return 0 if the password is too short
# return 1 if the password does not contain any digits
# return 2 if the password has no uppercase characters
# return 3 if the password has no symbols
# return 4 otherwise
def check_valid_password(password):
    too_short = len(password) < 7
    num_digits = len(re.findall(r"\d", password)) #maybe try findall?
    num_uppercase = len(re.findall(r"[A-Z]", password))
    num_lowercase = len(re.findall(r"[a-z]", password))
    num_symbols = len(re.findall(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password))

    if(too_short):
        return 0
    elif(num_digits < 1):
        return 1
    elif(num_uppercase < 1):
        return 2
    elif(num_symbols < 1):
        return 3
    else:
        return 4

# encrypt passwords with a randomly generated salt then hash.
# returns the password as a unicode string
def encrypt_pass(pswrd):
    encoded_pswrd = pswrd.encode('utf-8')
    random_salt = bcrypt.gensalt(rounds=12)    # rounds specify length of salt
                   
    hashed_pswrd = bcrypt.hashpw(encoded_pswrd, random_salt).decode('utf-8', 'strict')
    return hashed_pswrd

# checks an inputted password against its encrypted hash. returns
# true if a match if found, false otherwise
def check_pass(pswrd, hash_pswrd):
    encoded_pswrd = pswrd.encode('utf-8')
    encoded_hash_pswrd = hash_pswrd.encode('utf-8')

    return bcrypt.checkpw(encoded_pswrd, encoded_hash_pswrd)

# updates a column in the user database with new information and a user_id
def update_user_info(newInfo, var_to_change, user_id = None, oldInfo = None):
    conn = sqlite3.connect(db_path)

    update_group_info = ""

    update_user_info = "UPDATE users SET {} = ? WHERE user_id = ?".format(var_to_change)
    
    if(var_to_change == 'username'):
        print(oldInfo + " has changed their name to " + newInfo)

    if(var_to_change == 'password'):
        newInfo = encrypt_pass(newInfo)

    cursor = conn.cursor()
    cursor.execute(update_user_info, (newInfo, user_id))

    if(update_group_info != ""):
        cursor.execute(update_group_info, ('group_name', oldInfo, newInfo))
    
    conn.commit()
    conn.close()

# updates a column in the group database with new information and a group_id
def update_group_info(newInfo, var_to_change, group_id):
    conn = sqlite3.connect(db_path)

    if(var_to_change == 'group_name'):
        update_user_info = "UPDATE groups SET {} = ? WHERE group_id = ?".format(var_to_change)

    cursor = conn.cursor()
    cursor.execute(update_user_info, (newInfo, group_id))
    
    conn.commit()
    conn.close()

def create_group_id():
    group_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)]) 
    return group_id

def join_group(group_id, group_name, user_id, group_type = 'group'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    checkTableExists(conn, 'groups')

    c.execute("INSERT INTO groups VALUES (?, ?, ?, ?)", (group_id, group_name, user_id, group_type))
    conn.commit()
    conn.close()

def leave_group(group_id, user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    checkTableExists(conn, 'groups')

    leave_cmd = "DELETE from groups WHERE group_id=? AND member_id=?"
    c.execute(leave_cmd, (group_id, user_id))
    
    conn.commit()
    conn.close()

def get_group_name(group_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    checkTableExists(conn, 'groups')
    groupName = ""

    c.execute("SELECT group_name FROM groups WHERE group_id=?" , (group_id,))
    groupName = c.fetchone()[0]

    conn.close()
    return groupName

def retrieve_group_members(group_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    checkTableExists(conn, 'groups')

    c.execute("SELECT member_id FROM groups WHERE group_id=?", (group_id,))

    list_of_users = c.fetchall()

    return list_of_users