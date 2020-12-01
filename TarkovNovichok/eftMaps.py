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
from TarkovNovichok import spotifyControl

# Path of tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
windowHwnd = win32gui.FindWindow(None, 'EscapeFromTarkov')

root = Tk()
root.geometry("1220x720")
root.configure(bg='black')
root.title('Tarkov Novichok')

def getMapImagePath(argument):
    if not argument:
        return None
    switcher = {
        'reserve': resource_path('reserveMap.jpg'),
        'customs': resource_path('customs.png'),
        'factory': resource_path('factory.png'),
        'interchange': resource_path('interchange.jpg'),
        'shoreline': resource_path('shoreline.png'),
        'woods': resource_path('woods.png')
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

def watchForMapName():
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
            x = windowSize[0]
            y = windowSize[1]
            w = windowSize[2] - x
            h = windowSize[3] - y
            widthModifier = w/2.45
            heigthModifier = h/1.17
            adjustedSize = ((x+widthModifier+50), (y+h/9.83),
                            (windowSize[2]-widthModifier), (windowSize[3]-heigthModifier))

            # ImageGrab-To capture the screen image in a loop.
            # Bbox used to capture a specific area.
            cap = ImageGrab.grab(adjustedSize)
            # cap.show()

            # Converted the image to monochrome for it to be easily
            # read by the OCR and obtained the output String.
            parsedText = pytesseract.image_to_string(
                cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),
                lang='eng')
            mapPath = getMapImagePath(parsedText)
            global currentMapImg
            if mapPath is not None and mapPath != currentMapImg:
                openMapImage(mapPath)
                currentMapImg = mapPath

    root.after(1000, watchForMapName)

def watchForRaidStatus():
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
            x = windowSize[0]
            y = windowSize[1]
            w = windowSize[2] - x
            h = windowSize[3] - y
            widthModifier = w/2.7
            heigthModifier = h/1.115
            adjustedSize = ((x+widthModifier), (y),
                            (windowSize[2]-widthModifier), (windowSize[3]-heigthModifier))

            # ImageGrab-To capture the screen image in a loop.
            # Bbox used to capture a specific area.
            cap = ImageGrab.grab(adjustedSize)
            # cap.show()

            # Converted the image to monochrome for it to be easily
            # read by the OCR and obtained the output String.
            parsedText = pytesseract.image_to_string(cap,
                                                        lang='eng')
            print(parsedText)
            parsedText = parsedText.lower()
            if 'deploying to location' in parsedText:
                spotifyControl.pauseSpotify()
            elif 'raid ended' in parsedText:
                spotifyControl.playSpotify()
    root.after(4500, watchForRaidStatus)

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
    return os.path.join(os.path.abspath(".\\maps"), relative_path)

currentMapImg = resource_path('offline.jpg')

im = Image.open(resource_path('offline.jpg'))
currentImage = im.copy()
img = ImageTk.PhotoImage(im)
panel = Label(root, image=img, bg="black")
panel.image = img
panel.bind('<Configure>', resize_image)
panel.pack(fill="both", expand="yes")

root.after(1000, watchForMapName)
root.after(4500, watchForRaidStatus)
root.mainloop()
