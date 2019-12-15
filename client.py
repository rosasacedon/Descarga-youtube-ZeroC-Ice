#!/usr/bin/env python3
# -*- coding: utf-8; -*-
'''
Implementacion cliente
'''

import sys
import Ice # pylint: disable=E0401,E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

class Client(Ice.Application):
    '''
    Clase cliente
    '''
    def descargar_cancion(self, orchestrator, url, current=None):
        ''' Descargar cancion '''
        orchestrator.downloadTask(url)
 

    def get_list(self, orchestrator, current=None):
        ''' obtener lista '''
        lista = []
        lista = orchestrator.getFileList()
        print(lista)

    def run(self, argv):
        ''' Run '''
        proxy = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)
        if not orchestrator:
            raise RuntimeError("Invalid proxy")
        
        if len(argv) == 2:
            self.get_list(orchestrator)
            sys.exit()
        
        self.descargar_cancion(orchestrator, argv[2])



sys.exit(Client().main(sys.argv))
