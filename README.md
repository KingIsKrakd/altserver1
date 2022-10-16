# Ez-AltServer-Linux
I tried to install and use Altserver linux and while it was cool, it was a huge pain. This is an application designed to make installation & usage easy.

This is also a project I'm using to get more comfortable with python.

The Install AltStore feature is untested, but feel free to try it.
# Usage
1.Download the latest binary of [Altserver-Linux](https://github.com/NyaMisty/AltServer-Linux/releases) for your platform and place it here (tested with v0.0.5 if you run into issues)

2.Download the latest binary of [Anisette-server](https://github.com/Dadoum/Provision/releases) for your platform and place it here (You don't need libprovision, only anisette_server)

3. Download the Apple Music APK and extract it. Place the lib directory in the same directory as the rest of the files. You can delete every folder except your architecture and every file in that folder except libstoreservicescore.so and libCoreADI.so. For more info, check out [Provision](https://github.com/Dadoum/Provision).

4. As long as you have python 3.8 and tkinter, you can just run main.py. If you have issues with the device UDID, use the -u flag to specify it manually.
