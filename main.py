import atexit
import subprocess
import time
from tkinter import*
import tkinter.messagebox
import os
import sys

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

anisette_proc = subprocess.Popen("./anisette_server", close_fds=True)
#Bad practice I know. Give time for anisette to start up
time.sleep(2)

env = dict(os.environ)
env["ALTSERVER_ANISETTE_SERVER"] = "http://127.0.0.1:6969"

alt_proc = subprocess.Popen("./AltServer", close_fds=True, env=env)

def exit_handler():
    print("Killing anisette & altserver")
    subprocess.Popen.kill(anisette_proc)
    subprocess.Popen.kill(alt_proc)

atexit.register(exit_handler)
root = tkinter.Tk()

def runInstall(top, email, password, udid):
    top.destroy()
    command = "./AltServer --udid " + udid + " -a " + email + " -p " + password + " 1_5.ipa"
    print(command)
    test = tkinter.messagebox.askokcancel(title="AltStore", message="This will install AltStore on your device. Enter the 2fa code in the terminal that you ran this with. This is untested, if it doesn't work open a github issue and run the command that is currently in the terminal.")

    if(test == True):
        subprocess.Popen.kill(alt_proc)
        try:
            subprocess.Popen(command, close_fds=True, shell=True, env=env).wait()
        except subprocess.CalledProcessError:
            tkinter.messagebox.showinfo(title="Error", message="Error installing AltStore. Check the terminal for more info. This program will now exit.")
            exit()
        alt_proc = subprocess.Popen("./AltServer", close_fds=True, env=env)
    

def popupwin(udid):
    test = tkinter.messagebox.askyesno(title="UDID", message="Is the following device UDID Correct? (If unsure, press yes): " + udid)

    if(test == False):
        tkinter.messagebox.showinfo(title="UDID", message="Specify the UDID of your device with the -u flag")
        return 
    top = Toplevel(root)
    top.title("Apple ID")
    top.geometry("250x100")
    # add email label
    emailLabel = Label(top, text="Email")
    emailLabel.grid(row=0, column=0)
    email = Entry(top, width=21)
    email.grid(row=0, column=1)

    # add password label
    passwordLabel = Label(top, text="Password")
    passwordLabel.grid(row=1, column=0)
    password = Entry(top, width=21)
    password.grid(row=1, column=1)

    button= Button(top, text="Ok", command=lambda:runInstall(top, email.get(), password.get(), udid))
    button.grid(row=2, column=1)

def installAltStore():
    tkinter.messagebox.showinfo(title="AltStore", message="This will now download AltStore 1.5")
    # Check if 1_5.ipa exists
    if(os.path.isfile("1_5.ipa") == False):
        try:
            subprocess.Popen("wget https://cdn.altstore.io/file/altstore/apps/altstore/1_5.ipa", close_fds=True, shell=True).wait()
        except subprocess.CalledProcessError:
            tkinter.messagebox.showinfo(title="Error", message="Error downloading AltStore. Check the terminal for more info. If the issue persists, download AltStore ipa from https://cdn.altstore.io/file/altstore/apps/altstore/1_5.ipa manually.")
            exit()
    # check if -u flag is present
    if(len(sys.argv) == 3):
        if(sys.argv[1] == "-u"):
            popupwin(sys.argv[2])
            return
    try:
        udid = subprocess.check_output("idevice_id -l", shell=True)
    except subprocess.CalledProcessError:
        tkinter.messagebox.showinfo(title="UDID Error", message="Error getting UDID: Is your device connected? Is libimobiledevice-utils installed? (If you don't want/can't install it, specify a udid on the command line with flag -u")
        return

    udid = udid.decode("utf-8")
    udid = udid.strip()

    popupwin(udid)
    


root.title("AltServer")
root.geometry("500x200")
root.resizable(False, False)

altstoreImg = tkinter.PhotoImage(file="altserver.png")
altstoreImg = altstoreImg.subsample(3, 3)
imgLabel = tkinter.Label(root, image=altstoreImg)
imgLabel.place(x=5, y=5)

# Add main text
mainText = tkinter.Label(root, text="AltServer is running in the background. To install apps, open AltStore on your iOS device.", font=("Helvetica", 12), wraplength=375)
mainText.place(x=125, y=40)

# Add quit button
quitButton = tkinter.Button(root, text="Quit", command=root.destroy)
quitButton.place(x=360, y=95)

# Add install altstore button
installAltstoreButton = tkinter.Button(root, text="Install AltStore", command=installAltStore)
installAltstoreButton.place(x=160, y=95)

# Add credits label
creditsLabel0 = tkinter.Label(root, text="This gui by nab138", font=("Helvetica", 8))
creditsLabel0.place(x=2, y=150)
creditsLabel1 = tkinter.Label(root, text="AltServer by Riley Testut", font=("Helvetica", 8))
creditsLabel1.place(x=2, y=162)
creditsLabel2 = tkinter.Label(root, text="Anisette-server by Dadoum", font=("Helvetica", 8))
creditsLabel2.place(x=2, y=174)
creditsLabel3 = tkinter.Label(root, text="AltServer-Linux by NyaMisty", font=("Helvetica", 8))
creditsLabel3.place(x=2, y=186)
root.mainloop()

