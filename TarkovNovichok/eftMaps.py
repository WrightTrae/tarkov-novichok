# cv2.cvtColor takes a numpy ndarray as an argument
import numpy as nm
from tkinter import Tk, Label, Frame
import pytesseract
import pathlib
import win32gui
import win32con
import re
import os
import sys

# importing image parsing/ reading
import cv2
from PIL import ImageGrab, Image, ImageWin, ImageTk, ImageOps

# Spotify Controls
from TarkovNovichok import spotifyControl, const

# Path of tesseract executable
pytesseract.pytesseract.tesseract_cmd = '.\\Tesseract-OCR\\tesseract.exe'
windowHwnd = win32gui.FindWindow(None, 'EscapeFromTarkov')

status = const.INITIAL_STATUS

root = Tk()
root.geometry("1220x720")
root.configure(bg='black')
root.title('Tarkov Novi')


def getImagePath(argument):
    if not argument:
        return None
    switcher = {
        'reserve': resource_path('.\\maps\\reserve.jpg'),
        'customs': resource_path('.\\maps\\customs.png'),
        'factory': resource_path('.\\maps\\factory.png'),
        'interchange': resource_path('.\\maps\\interchange.jpg'),
        'shoreline': resource_path('.\\maps\\shoreline.png'),
        'woods': resource_path('.\\maps\\woods.png'),
        'offline': resource_path('.\\maps\\offline.jpg'),
        'ammo': resource_path('.\\maps\\ammo.png')
    }
    result = re.sub(r'[^A-Za-z]', '', argument)
    result = result.lower()

    if len(result) == 0:
        return None

    firstLetter = result[0]
    if firstLetter == 'e':
        result = result[1:]
    return switcher.get(result, None)


def openMapImage(path):
    im = Image.open(path)
    global currentImage
    rootHeight = root.winfo_reqheight()
    rootWidth = root.winfo_reqwidth()
    im = im.resize((rootWidth, rootHeight))
    currentImage = im.copy()
    img = ImageTk.PhotoImage(im)
    panel.configure(image=img)
    panel.image = img


def cropCap(screenCap, size):
    cap = screenCap.crop(size)
    # cap.show()
    return cap


def parseMapName(cap, windowSize):
    print('# parseMapName')
    x = windowSize[0]
    y = windowSize[1]
    w = windowSize[2] - x
    h = windowSize[3] - y
    cropedCap = cropCap(
        cap, (w/2.15, h/10.5, w/1.75, h/7))
    parsedText = pytesseract.image_to_string(
        cv2.cvtColor(nm.array(cropedCap), cv2.COLOR_BGR2GRAY),
        lang='eng')
    print(parsedText)
    mapPath = getImagePath(parsedText)
    global currentMapImg
    if mapPath is not None and mapPath != currentMapImg:
        openMapImage(mapPath)
        currentMapImg = mapPath


def parseRaidStatus(cap, windowSize):
    print('# parseRaidStatus')
    x = windowSize[0]
    y = windowSize[1]
    w = windowSize[2] - x
    h = windowSize[3] - y
    cropedCap = cropCap(
        cap,  (w/2.7, 0, w/1.6, h/9.5))
    parsedText = pytesseract.image_to_string(
        cv2.cvtColor(nm.array(cropedCap), cv2.COLOR_BGR2GRAY),
        lang='eng')
    print(parsedText)
    parsedText = parsedText.lower()

    global status
    if 'deploying to location' in parsedText:
        status = const.IN_RAID
    elif 'raid ended' in parsedText:
        status = const.RAID_ENDED
    elif 'prepare to escape' in parsedText:
        status = const.RAID_PREPARE


def readScreen():
    if windowHwnd:
        tup = win32gui.GetWindowPlacement(windowHwnd)
        minimized = True
        if tup[1] == win32con.SW_SHOWMAXIMIZED:
            minimized = False
        elif tup[1] == win32con.SW_SHOWMINIMIZED:
            minimized = True
        elif tup[1] == win32con.SW_SHOWNORMAL:
            minimized = False

        if not minimized:
            windowSize = win32gui.GetWindowRect(windowHwnd)
            cap = ImageGrab.grab(windowSize)

            # Raid Status
            parseRaidStatus(cap, windowSize)

            global status
            if status == const.RAID_PREPARE:
                # Map Name
                parseMapName(cap, windowSize)

            elif status == const.IN_RAID:
                spotifyControl.pauseSpotify()

            elif status == const.RAID_ENDED:
                spotifyControl.playSpotify()
                offlinePath = getImagePath('offline')
                global currentMapImg
                if offlinePath != currentMapImg:
                    openMapImage(offlinePath)
                    currentMapImg = offlinePath


def startReadLoop():
    readScreen()
    root.after(2000, startReadLoop)


def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = currentImage.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    panel.config(image=photo)
    panel.image = photo  # avoid garbage collection


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


currentMapImg = getImagePath('ammo')

im = Image.open(currentMapImg)
currentImage = im.copy()
img = ImageTk.PhotoImage(im)
panel = Label(root, image=img, bg="black")
panel.image = img
panel.bind('<Configure>', resize_image)
panel.pack(fill="both", expand="yes")

root.after(1000, startReadLoop)
root.mainloop()
