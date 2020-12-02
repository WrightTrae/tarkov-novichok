import sys
import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import socket
import configparser
from importlib import resources

cfg = configparser.ConfigParser()
cfg.read('config.cfg')
clientId = cfg.get('spotifyControl', 'CLIENT_ID')
clientSecret = cfg.get('spotifyControl', 'CLIENT_SECRET')
redirectUrl = cfg.get('spotifyControl', 'REDIRECT_URL')

client_credentials_manager = SpotifyOAuth(client_id=clientId,
                                          client_secret=clientSecret,
                                          redirect_uri=redirectUrl,
                                          scope="user-read-playback-state,user-modify-playback-state")
auth = ''


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
