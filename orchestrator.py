#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import Ice
Ice.loadSlice('trawlnet.ice')
import sys
import TrawlNet

class Orchestrator(TrawlNet.Orchestrator):
    def __init__(self, downloader):
        self.downloader = downloader

    def downloadTask(self, url, current=None):
        print('url que se va a descargar ',url)
        mensaje = self.downloader.addDownloadTask(url)
        print("Downloader responde ",mensaje)

        return mensaje


class Server(Ice.Application):

    def run(self, argv):

        print('Iniciando orquestador')
        broker = self.communicator()
        prx_downloader = broker.stringToProxy(argv[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(prx_downloader)

        if not downloader:
            raise RuntimeError('Proxy no valido')

        # Obteniendo el proxy y creando el objeto
        orquestador = Orchestrator(downloader)
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        proxy = adapter.add(orquestador, broker.stringToIdentity("orchestrator"))

        print("'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

server = Server()
sys.exit(server.main(sys.argv))
