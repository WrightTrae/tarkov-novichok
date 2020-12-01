import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import socket
from decouple import config

auth = ''
client_credentials_manager = SpotifyOAuth(client_id=config('CLIENT_ID'),
                                          client_secret=config(
                                              'CLIENT_SECRET'),
                                          redirect_uri=config('REDIRECT_URL'),
                                          scope="user-read-playback-state,user-modify-playback-state")


def playSpotify():
    try:
        sp = spotipy.Spotify(
            auth=auth, client_credentials_manager=client_credentials_manager)
        playback = sp.current_playback()
        devices = sp.devices()
        pcId = getPcId(devices['devices'])
        if playback == None or not playback["is_playing"]:
            sp.start_playback(device_id=pcId)
    except:
        print('Error starting playback')


def pauseSpotify():
    try:
        sp = spotipy.Spotify(
            auth=auth, client_credentials_manager=client_credentials_manager)
        playback = sp.current_playback()
        devices = sp.devices()
        pcId = getPcId(devices['devices'])
        if playback["is_playing"]:
            sp.pause_playback(device_id=pcId)
    except:
        print('Error pausing playback')


def getPcId(deviceList):
    pcName = socket.gethostname()
    for device in deviceList:
        if device["name"] == pcName:
            return device["id"]
