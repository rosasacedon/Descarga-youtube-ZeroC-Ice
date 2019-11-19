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
        msg = intermediate.downloadTask(url)
        print("Manager reply "+msg)

    def run(self, argv):
         proxy = self.communicator().stringToProxy(argv[1])
         orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)
         if not orchestrator:
             raise RuntimeError("Invalid proxy")

         self.download_song(intermediate=orchestrator, url=argv[2])


sys.exit(Client().main(sys.argv))