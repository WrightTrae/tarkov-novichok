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

# Path of tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
windowHwnd = win32gui.FindWindow(None, 'EscapeFromTarkov')

def cropCap(screenCap, windowSize, size):
    cap = screenCap.crop(size)
    cap.show()
    return cap


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
            x = windowSize[0]
            y = windowSize[1]
            w = windowSize[2] - x
            h = windowSize[3] - y

            # Map Name
            mapNameCrop = cropCap(
                cap, windowSize, (w/2.15, h/8.45, w/1.75, h/6.8))

            # Raid Status
            raidStatusCrop = cropCap(
                cap, windowSize,  (w/2.7, 0, w/1.6, h/9.2))


readScreen()
