# Ez-AltServer-Linux
I tried to install and use Altserver linux and while it was cool, it was a huge pain. This is an application designed to make usage easy.

Important Notes:
1. It is not advised to use your main apple id with this, as it is experimental.
2. This project is designed to run on x86_64 and has only been confirmed working on Linux mint 20.2 cinnamon (testing other distros/de's soon)
3. If you are going to run on platforms other than x86_64 you will have to manually download anisette_server and AltServer for now, this will hopefully be fixed later
4. I'm not a python developer, you will run into stupid issues. If you open an issue on github I will try to fix them.

This is also a project I'm using to get more comfortable with python. I barely did anything here, all credit goes to NyaMisty for making AltServer-Linux. I just made a simple python script to make it easier to use.

You can contact me on discord or open a github issue if you have any problems: `nab138#2035`
# Install Instructions
1. Clone this repo

2. Use pip to install the requirments from requirements.txt `pip install -r requirements.txt`

3. As long as you have python 3.8 and tkinter, you can just run main.py and follow the instructions. If you have issues with the device UDID, use the -u flag to specify it manually.

# Usage
When the program is running, so is altserver-linux and anisette server. Install altstore does as it says, but requires the program to be run via terminal to input the 2fa code (may be fixed later if enough interest for this repo is found)

Closing the window will minimize it to tray, where it can be quit or maximized. It does NOT kill altserver or anisette.

If your trying to do things like netmuxd, any env variables you set will be passed to altserver-linux (but not anisette_Server)
# Future Plans
In the near future I plan to:
- [x] Automate install of libraries
- [x] Setup pyinstaller to build binaries
- [x] Fix tray issue
- [x] Fix install altstore
- [x] Add pair button
- [x] Add restart usbmuxd button
- [x] Fix threading quit issue

I will publish a release shortly

Some point in the future I plan to:
- [ ] Add a box to enter the 2fa code in the gui
- [ ] Detect platform to download the correct binaries for anisette_server and AltServer, and save on space with the apple music libs


Will not impliment:
- Saving username/password - Don't want to mess with doing it securly and it isn't really neccessary, since altstore on device saves the apple id password. You only need to press install altstore once or twice and typing your password manually is easy enough

# Screenshots

![AltServer GUI](https://nab138.tixte.co/r/altserver.png)

# Credits

[Provision](https://github.com/Dadoum/Provision)

[AltServer-linux](https://github.com/NyaMisty/AltServer-Linux)

[AltStore](https://altstore.io/)