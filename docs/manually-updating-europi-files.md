# Manually updating software on the EuroPi

## Install Thonny

1. Download from here: https://thonny.org/ (Windows, Mac and Linux versions available)
2. Install using the setup routine:
	- Mac: Double click the pkg file and follow instructions
	- Windows: Double click the exe file and follow instructions
	- Linux: The best method is using python pip: `python3 -m pip install thonny`

## Connecting the EuroPi to your computer

You will need a Micro-usb cable like the one shown here: https://thepihut.com/products/usb-to-micro-usb-cable-0-5m

1. Connect the micro end of the cable to the micro-usb connection on the rear of the EuroPi at the very top
2. Connect the other end to your computer
3. Open Thonny, then click the "Stop" button to connect
4. When you are successfully connected you will see text similar to the text below in the bottom Thonny window

```
MicroPython v1.18 on 2022-01-17; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> 
```

**Note**: Sometimes you need to disconnect and reconnect the EuroPi to make a successful connection. For example if you see the error below.

```
Couldn't find the device automatically. 
Check the connection (making sure the device is not in bootloader mode) or choose
"Configure interpreter" in the interpreter menu (bottom-right corner of the window)
to select specific port or another interpreter.
```

## Copying and updating files

1. Click the "Open" icon in the top Thonny menu, or click File->Open
2. Click "This computer" to open the file you want to copy to the EuroPi
3. Browse to the file you want to copy to the EuroPi, this will open the file in the editor window
4. Choose File->Save as, then select "Raspberry Pi Pico" as the destination
5. Browse to the location to save the file to, enter the required filename, then click "OK"