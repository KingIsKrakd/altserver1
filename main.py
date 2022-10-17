import atexit
import subprocess
import time
from tkinter import*
import tkinter.messagebox
from pystray import MenuItem as item
import pystray
import os
import argparse
from PIL import Image
import platform

print("platform.architecture() = " , platform.architecture())
parser = argparse.ArgumentParser(description='Install AltStore on your device')
parser.add_argument('-u', help='Specify the UDID of your device manually. Will bypass any libimobiledevice-utils calls.')
args = parser.parse_args()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if(os.path.isfile("AltServer") == False):
    tkinter.messagebox.showinfo(title="AltServer", message="Will download the latest release of AltStore for ")
    try:
        subprocess.Popen("wget https://cdn.altstore.io/file/altstore/apps/altstore/1_5.ipa", close_fds=True, shell=True).wait()
    except subprocess.CalledProcessError:
        tkinter.messagebox.showinfo(title="Error", message="Error downloading AltStore. Check the terminal for more info. If the issue persists, download AltStore ipa from https://cdn.altstore.io/file/altstore/apps/altstore/1_5.ipa manually.")
        exit()

#anisette_proc = subprocess.Popen("./anisette_server", close_fds=True)
#Bad practice I know. Give time for anisette to start up
time.sleep(2)

env = dict(os.environ)
env["ALTSERVER_ANISETTE_SERVER"] = "http://127.0.0.1:6969"

#alt_proc = subprocess.Popen("./AltServer", close_fds=True, env=env)

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
    test = tkinter.messagebox.askokcancel(title="AltStore", message="Enter the 2fa code in the terminal that you ran this with. This is untested, if it doesn't work open a github issue and run the command that is currently in the terminal.")

    if(test == True):
        subprocess.Popen.kill(alt_proc)
        try:
            subprocess.Popen(command, close_fds=True, shell=True, env=env).wait()
        except subprocess.CalledProcessError:
            tkinter.messagebox.showinfo(title="Error", message="Error installing AltStore. Check the terminal for more info. This program will now exit.")
            exit()
        alt_proc = subprocess.Popen("./AltServer", close_fds=True, env=env)
    

def popupwin(udid, name):
    test = tkinter.messagebox.askokcancel(title="UDID", message="Install AltStore onto the device \"" + name + "\" with the UDID \"" + udid + "\"?")

    if(test == False):
        return 
    top = Toplevel(root)
    top.title("Apple ID")
    top.geometry("250x100")

    emailLabel = Label(top, text="Email")
    emailLabel.grid(row=0, column=0)
    email = Entry(top, width=21)
    email.grid(row=0, column=1)

    passwordLabel = Label(top, text="Password")
    passwordLabel.grid(row=1, column=0)
    password = Entry(top, width=21)
    password.grid(row=1, column=1)

    button = Button(top, text="Ok", command=lambda:runInstall(top, email.get(), password.get(), udid))
    button.grid(row=2, column=1)

def installAltStore():
    if(os.path.isfile("1_5.ipa") == False):
        tkinter.messagebox.showinfo(title="AltStore", message="This will now download AltStore 1.5")
        try:
            subprocess.Popen("wget https://cdn.altstore.io/file/altstore/apps/altstore/1_5.ipa", close_fds=True, shell=True).wait()
        except subprocess.CalledProcessError:
            tkinter.messagebox.showinfo(title="Error", message="Error downloading AltStore. Check the terminal for more info. If the issue persists, download AltStore ipa from https://cdn.altstore.io/file/altstore/apps/altstore/1_5.ipa manually.")
            exit()

    if(args.u != None):
        popupwin(args.u, "Unknown")
        return
        
    try:
        udid = subprocess.check_output("idevice_id -l", shell=True)
        name = subprocess.check_output("ideviceinfo -k DeviceName", shell=True)
    except subprocess.CalledProcessError:
        tkinter.messagebox.showinfo(title="Device Error", message="Error communicating with device: Is your device connected? Is libimobiledevice-utils installed?")
        return

    udid = udid.decode("utf-8")
    udid = udid.strip()
    name = name.decode("utf-8")
    name = name.strip()
    popupwin(udid, name)
    


root.title("AltServer")
root.geometry("500x180")
root.resizable(False, False)
root.iconphoto(True, PhotoImage(file="altserver.png"))

altstoreImg = tkinter.PhotoImage(file="altserver.png")
altstoreImg = altstoreImg.subsample(3, 3)
imgLabel = tkinter.Label(root, image=altstoreImg)
imgLabel.place(x=5, y=5)

# Add main text
mainText = tkinter.Label(root, text="AltServer is running in the background. To install apps, open AltStore on your iOS device. Closing this window will minimize to tray.", font=("Helvetica", 12), wraplength=370)
mainText.place(x=125, y=30)

# Add quit button
quitButton = tkinter.Button(root, text="Quit", command=root.destroy)
quitButton.place(x=360, y=95)

# Add install altstore button
installAltstoreButton = tkinter.Button(root, text="Install AltStore", command=installAltStore)
installAltstoreButton.place(x=160, y=95)

# Add credits label
creditsLabel0 = tkinter.Label(root, text="This gui by nab138", font=("Helvetica", 8))
creditsLabel0.place(x=2, y=130)
creditsLabel1 = tkinter.Label(root, text="AltServer by Riley Testut", font=("Helvetica", 8))
creditsLabel1.place(x=2, y=142)
creditsLabel2 = tkinter.Label(root, text="Anisette-server by Dadoum", font=("Helvetica", 8))
creditsLabel2.place(x=2, y=154)
creditsLabel3 = tkinter.Label(root, text="AltServer-Linux by NyaMisty", font=("Helvetica", 8))
creditsLabel3.place(x=2, y=166)

def quit_window(icon, item):
   icon.stop()
   root.destroy()

# Define a function to show the window again
def show_window(icon, item):
   icon.stop()
   root.after(0,root.deiconify())

# Hide the window and show on the system taskbar
def hide_window():
   root.withdraw()
   image=Image.open("altserver.ico")
   menu=(item('Quit', quit_window), item('Show', show_window))
   icon=pystray.Icon("name", image, "AltServer", menu)
   icon.run()

root.protocol('WM_DELETE_WINDOW', hide_window)

root.mainloop()