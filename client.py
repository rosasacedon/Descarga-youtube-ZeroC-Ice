#!/usr/bin/env python3
# -*- coding: utf-8; -*-
'''
Client
'''

import sys
import Ice # pylint: disable=E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class Client(Ice.Application):
    '''
    Clase cliente
    '''
    def descargar_cancion(self, orchestrator, url, current=None): # pylint: disable=W0613
        ''' Descargar cancion '''
        orchestrator.downloadTask(url)
        
    def run(self, argv):
        ''' Run '''
        lista = []
        proxy = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)
        if not orchestrator:
            raise RuntimeError("Invalid proxy")
        
        if len(argv) == 2:
            lista = orchestrator.getFileList()
            print(lista)
            sys.exit()
        
        self.descargar_cancion(orchestrator, argv[2])



sys.exit(Client().main(sys.argv))
