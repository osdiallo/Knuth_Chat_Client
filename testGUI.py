#Beginings of the sign in page

import tkinter as tk

#functions
def click(event): #handles click for username
    if Name_entry.get() == "Username":
        Name_entry.delete(0, "end")
        Name_entry.insert(0, "")
        Name_entry.config(fg = "black")
def clickP(event): #handles click for Password
    if Pass_entry.get() == "Password":
        Pass_entry.delete(0, "end")
        Pass_entry.insert(0, "")
        Pass_entry.config(fg = "black", show="*")

def clickout(event): #handles clicking out of username
    if Name_entry.get() == "":
        Name_entry.insert(0, "Username")
        Name_entry.config(fg = "grey")
def clickoutP(event): #handles clicking out of password
    if Pass_entry.get() == "":
        Pass_entry.insert(0, "Password")
        Pass_entry.config(fg = "grey", show="")
        
def LogInClick():
    if((Name_entry.get() == "") or (Pass_entry.get() == "") or (Name_entry.get() == "Username") or (Pass_entry.get() == "Password")):
        elabel.config(text="Incomplete Sign In!")
    else:
        elabel.config(text="")

app = tk.Tk()

bkc = "SeaGreen3"

app.config(background=bkc)

label = tk.Label(app, text="Knuth Konnections", bg=bkc)
label.config(width=200, font=("TkDefaultFont", 15))
#label.grid(columnspan=2, pady=(10,0))
label.pack()

Name = tk.Label(app, text="Username:", bg=bkc)
Pass = tk.Label(app, text="Password:", bg=bkc)

#Username Entry
Name_entry = tk.Entry(app)
Name_entry.insert(0, "Username")
Name_entry.bind("<FocusIn>", click)
Name_entry.bind("<FocusOut>", clickout)
Name_entry.config(fg = 'grey')

#Password Entry
Pass_entry = tk.Entry(app)
Pass_entry.insert(0, "Password")
Pass_entry.bind("<FocusIn>", clickP)
Pass_entry.bind("<FocusOut>", clickoutP)
Pass_entry.config(fg = 'grey')

Name_entry.pack(pady=5)
Pass_entry.pack(pady=5)

c = tk.Checkbutton(app, text="Remember me", bg=bkc)
c.pack()

sin = tk.Button(app, text="Sign In", bg="SlateGray2", command=LogInClick)
sin.pack()

elabel = tk.Label(app, text="", bg=bkc)
elabel.config(width=200, font=("TkDefaultFont", 10), foreground="red")
elabel.pack()

sup = tk.Label(app, text="New User? Sign up Today!", bg=bkc)
sup.pack()

nus = tk.Button(app, text="Sign Up", bg="SlateGray2")
nus.pack()

app.geometry("210x230")

app.mainloop()