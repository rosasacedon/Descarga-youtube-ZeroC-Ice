#!/usr/bin/env python3
# -*- coding: utf-8; -*-
'''
Implementacion cliente
'''
import os
import binascii

import sys
import Ice # pylint: disable=E0401,E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

APP_DIRECTORY = './'
DOWNLOADS_DIRECTORY = os.path.join(APP_DIRECTORY, 'downloads')

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




def transfer_request(self, file_name):
    remote_EOF = False
    BLOCK_SIZE = 1024
    transfer = None
    try:
        transfer = self.orchestrator.getFile(file_name)
    except TrawlNet.TransferError as e:
        print(e.reason)
        return 1
    with open(os.path.join(DOWNLOADS_DIRECTORY, file_name), 'wb') as file_:
        remote_EOF = False
        while not remote_EOF:
            data = transfer.recv(BLOCK_SIZE)
            if len(data) > 1:
                data = data[1:]
            data = binascii.a2b_base64(data)
            remote_EOF = len(data) < BLOCK_SIZE
            if data:
                file_.write(data)
        transfer.close()

    transfer.destroy()
    print('Transfer finished!')

sys.exit(Client().main(sys.argv))