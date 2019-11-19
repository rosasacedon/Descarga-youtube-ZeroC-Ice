#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import sys
import youtube_dl
import TrawlNet

class Downloader(TrawlNet.Downloader): 
    #esta clase y constructor
    def __init__(self):
        print("Downloader up")

    def addDownloadTask(self, url, current=None): 
        #addDownloadTask() es un metodo que añadirá una nueva tarea de descarga
        msg = "Starting download in "+url
        print(msg)
        self.download_song(url) 
        #download_song es una función que descarga la canción
        reply = "Download finished"
        return reply

    def download_song(self, url, current=None):
        print("Downloading....")

class Server(Ice.Application):
    def run(self, argv):
         #Running Downloader
        server = Downloader()
        broker = self.communicator()
        #Adding adapter
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy_server = adapter.add(server, broker.stringToIdentity("downloader"))
        print(proxy_server)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

server = Server()
sys.exit(server.main(sys.argv))