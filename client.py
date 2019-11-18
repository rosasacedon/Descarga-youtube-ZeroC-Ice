#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet

class Client(Ice.Application):
    def __init__(self):
        print("Client up")

    def download_song(self, intermediate, url, current=None): 
        #downoad_song es una función que mandará al intermediario la petición de descarga
        msg = intermediate.downloadTask(url)
        print("Manager reply "+msg)

    def run(self, argv):
         proxy = self.communicator().stringToProxy(argv[1])
         orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)