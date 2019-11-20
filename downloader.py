#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import sys
import youtube_dl
import TrawlNet
import download_mp3 as mp3

class Downloader(TrawlNet.Downloader): 
    #esta clase y constructor
    def __init__(self):
        print("Downloader up")

    def addDownloadTask(self, url, current=None): 
        #addDownloadTask() es un metodo que añadirá una nueva tarea de descarga
        msg = "Starting download in "+url
        print(msg) 
        #download_song es una función que descarga la canción
        return self.download_song(url)

    def download_song(self, url, current=None):
        print("Downloading....")
        mp3.download_mp3(url)

class Server(Ice.Application):
    def run(self, argv):
         #Running Downloader
        server = Downloader()
        broker = self.communicator()
        #Adding adapter
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy_server = adapter.add(server, broker.stringToIdentity("downloader"))
        print(proxy_server, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

server = Server()
sys.exit(server.main(sys.argv))
