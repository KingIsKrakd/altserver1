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
import sys
import threading

parser = argparse.ArgumentParser(description='Install AltStore on your device')
parser.add_argument('-u', help='Specify the UDID of your device manually. Will bypass any libimobiledevice-utils calls.')
args = parser.parse_args()

dname = os.path.dirname(sys.argv[0])
os.chdir(dname)

if(os.path.isfile("AltServer") == False):
	confirm = tkinter.messagebox.askokcancel(title="AltServer", message="Will download the latest release of AltServer Linux for x86_64. If you have a different platform download it manually and name it AltServer")
	if(confirm == False):
		sys.exit()
	try:
		subprocess.Popen("curl -L https://github.com/NyaMisty/AltServer-Linux/releases/latest/download/AltServer-x86_64 --output AltServer", close_fds=True, shell=True).wait()
		subprocess.Popen("chmod +x AltServer", close_fds=True, shell=True).wait()
		if(os.path.isfile("anisette_server") == True):
			tkinter.messagebox.showinfo(title="AltServer", message="Will now terminate. Please run this program again.")
			sys.exit()
	except subprocess.CalledProcessError:
		tkinter.messagebox.showinfo(title="Error", message="Error downloading AltServer. Check the terminal for more info. If the issue persists, download AltServer from https://github.com/NyaMisty/AltServer-Linux/releases/latest/download/AltServer-x86_64 manually.")
		sys.exit()
if(os.path.isfile("anisette_server") == False):
	confirm = tkinter.messagebox.askokcancel(title="AltServer", message="Will download the latest release of Anisette server for x86_64. If you have a different platform download it manually and name it anisette_server.")
	if(confirm == False):
		sys.exit()
	try:
		subprocess.Popen("curl -L https://github.com/Dadoum/Provision/releases/latest/download/anisette_server-x86_64 --output anisette_server", close_fds=True, shell=True).wait()
		subprocess.Popen("chmod +x anisette_server", close_fds=True, shell=True).wait()
		if(os.path.isdir("lib") == True):
			tkinter.messagebox.showinfo(title="AltServer", message="Will now terminate. Please run this program again.")
			sys.exit()
	except subprocess.CalledProcessError:
		tkinter.messagebox.showinfo(title="Error", message="Error downloading Anisette Check the terminal for more info. If the issue persists, download Anisette Server from https://github.com/Dadoum/Provision/releases/latest/download/anisette_server-x86_64 manually.")
		sys.exit()
if(os.path.isdir("lib") == False):
	confirm = tkinter.messagebox.askokcancel(title="AltServer", message="Will download the Apple music apk (Large file >100mb) and install the libs. The program will terminate after, you can restart it.")
	if(confirm == False):
		sys.exit()
	try:
		subprocess.Popen("curl -L https://apps.mzstatic.com/content/android-apple-music-apk/applemusic.apk --output music.apk", close_fds=True, shell=True).wait()
		subprocess.Popen("mkdir lib", close_fds=True, shell=True).wait()
		subprocess.Popen("unzip music.apk 'lib/*' -d .", close_fds=True, shell=True).wait()
		subprocess.Popen("rm music.apk", close_fds=True, shell=True).wait()
		sys.exit()
	except subprocess.CalledProcessError:
		tkinter.messagebox.showinfo(title="Error", message="Error downloading Apple Music. Check the terminal for more info. If the issue persists, download Apple Music from https://apps.mzstatic.com/content/android-apple-music-apk/applemusic.apk manually.")
		sys.exit()

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

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
	global alt_proc
	top.destroy()
	command = "./AltServer --udid " + udid + " -a " + email + " -p " + password + " 1_5.ipa"
	print(command)
	test = tkinter.messagebox.askokcancel(title="AltStore", message="After you click ok, a 2fa prompt should appear in the terminal. This is untested, if it doesn't work open a github issue and run the command that is currently in the terminal.")

	if(test == True):
		subprocess.Popen.kill(alt_proc)
		try:
			subprocess.Popen(command, close_fds=True, shell=True, env=env).wait()
		except subprocess.CalledProcessError:
			tkinter.messagebox.showinfo(title="Error", message="Error installing AltStore. Check the terminal for more info. This program will now exit.")
			sys.exit()
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
			subprocess.Popen("curl -o 1_5.ipa https://cdn.altstore.io/file/altstore/apps/altstore/1_5.ipa", close_fds=True, shell=True).wait()
		except subprocess.CalledProcessError:
			tkinter.messagebox.showinfo(title="Error", message="Error downloading AltStore. Check the terminal for more info. If the issue persists, download AltStore ipa from https://cdn.altstore.io/file/altstore/apps/altstore/1_5.ipa manually.")
			sys.exit()

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
	
def pair():
	try:
		subprocess.check_output("idevicepair pair", close_fds=True, shell=True)
	except subprocess.CalledProcessError as e:
		print(e.output.decode("utf-8"))
		if(e.output.decode("utf-8") == "No device found.\n"):
			tkinter.messagebox.showinfo(title="Pairing", message="Device is not connected")
		else:
			tkinter.messagebox.showinfo(title="Error", message="Error pairing with device. Ensure libimobiledevice-utils is installed. Check the terminal for more info.")
def restartUSB():
	try:
		subprocess.Popen("systemctl restart usbmuxd.service", close_fds=True, shell=True).wait()
	except subprocess.CalledProcessError:
		tkinter.messagebox.showinfo(title="Error", message="Error restarting usbmuxd. You may need to be root. Check the terminal for more info.")
	
root.title("AltServer")
root.geometry("500x180")
root.resizable(False, False)
root.iconphoto(True, PhotoImage(file=resource_path("altserver.png")))

altstoreImg = tkinter.PhotoImage(file=resource_path("altserver.png"))
altstoreImg = altstoreImg.subsample(3, 3)
imgLabel = tkinter.Label(root, image=altstoreImg)
imgLabel.place(x=5, y=5)

# Add main text
mainText = tkinter.Label(root, text="AltServer is running in the background. To install apps, open AltStore on your iOS device. Closing this window will minimize to tray.", font=("Helvetica", 12), wraplength=370)
mainText.place(x=125, y=30)


# Add install altstore button
installAltstoreButton = tkinter.Button(root, text="Install AltStore", command=installAltStore)
installAltstoreButton.place(x=125, y=95)

# Add pair button
quitButton = tkinter.Button(root, text="Pair", command=pair)
quitButton.place(x=265, y=95)

# Add quit button
quitButton = tkinter.Button(root, text="Restart usbmuxd", command=restartUSB)
quitButton.place(x=333, y=95)

# Add credits label
creditsLabel0 = tkinter.Label(root, text="This GUI by nab138", font=("Helvetica", 8))
creditsLabel0.place(x=2, y=130)
creditsLabel1 = tkinter.Label(root, text="AltServer by Riley Testut", font=("Helvetica", 8))
creditsLabel1.place(x=2, y=142)
creditsLabel2 = tkinter.Label(root, text="Anisette-server by Dadoum", font=("Helvetica", 8))
creditsLabel2.place(x=2, y=154)
creditsLabel3 = tkinter.Label(root, text="AltServer-Linux by NyaMisty", font=("Helvetica", 8))
creditsLabel3.place(x=2, y=166)
icon = None
quitEvent = threading.Event()
def hide_window():
   root.withdraw()
def quitSafe():
	root.destroy()
	if(icon != None):
		icon.stop()
	sys.exit()
def quit_window(icon, item):
	quitEvent.set()

def show_window(icon, item):
	if(root.state() == "withdrawn"):
		root.after(0, root.deiconify())
   
def installAltStoreTray(icon, item):
    show_window(icon, item)
    installAltStore()
image=Image.open(resource_path("altserver.ico"))
menu=(item("Install AltStore", installAltStoreTray), item('Show', show_window), item('Quit', quit_window))
icon=pystray.Icon("name", image, "AltServer", menu)
thread = threading.Thread(target=icon.run)
thread.start()


# Add quit button
quitButton = tkinter.Button(root, text="Quit", command=quitSafe)
quitButton.place(x=264, y=140)

root.protocol('WM_DELETE_WINDOW', hide_window)

def check_quits():
	if(quitEvent.is_set()):
		quitSafe()
	root.after(1000, check_quits)
check_quits()		

root.mainloop()
