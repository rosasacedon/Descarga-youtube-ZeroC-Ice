#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import sys
import TrawlNet

class Orchestrator(TrawlNet.Orchestrator):
    def __init__(self, dw):
        self.downloader = dw

    def downloadTask(self, url, current=None):
        print("Received url ->"+url)
        msg = self.downloader.addDownloadTask(url)
        return msg


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        proxy_downloader = broker.stringToProxy(argv[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(proxy_downloader)

        if not downloader:
            raise RuntimeError("Invalid Proxy")

        orch = Orchestrator(downloader)
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        proxy_orch = adapter.addWithUUID(orch)
        print(proxy_orch)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

server = Server()
sys.exit(server.main(sys.argv))
