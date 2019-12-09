#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Orchestrator
'''

import sys
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

canciones = []

class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Serer
    '''

    def run(self, argv):
        '''
        Iniciar
        '''
        key = "IceStorm.TopicManager.Proxy"
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            return None
        print("Using IceStorm in '%s'" % key)

        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(proxy)

        if not topic_mgr:
            return 2
        broker = self.communicator()
        proxy = broker.stringToProxy(argv[1])
        downloader_instance = TrawlNet.DownloaderPrx.checkedCast(proxy)
        if not downloader_instance:
            raise RuntimeError('Invalid proxy instance')

        evento_ficheros = UpdateEventI()
        files = evento_ficheros.files
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        fich_event = adapter.addWithUUID(evento_ficheros)
        topic_name = "UpdateEvents"
        qos = {}

        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        topic.subscribeAndGetPublisher(qos, fich_event)

        evento_orchestrators = OrchestratorEventI()
        evt_orchestrators = adapter.addWithUUID(evento_orchestrators)
        topic_orchestrator = "OrchestratorSync"
        qos_orc = {}
        try:
            topic_orch = topic_mgr.retrieve(topic_orchestrator)
        except IceStorm.NoSuchTopic:
            topic_orch = topic_mgr.create(topic_orchestrator)

        topic_orch.subscribeAndGetPublisher(qos_orc, evt_orchestrators)

        orchestrator = OrchestratorI(files)
        prx_orch = adapter.add(orchestrator, broker.stringToIdentity("orchestrator"))
        orchestrator.setProxy(prx_orch)
        orchestrator.set_params(downloader_instance, topic_orch, prx_orch)
        print(prx_orch)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0



class UpdateEventI(TrawlNet.UpdateEvent):
    files = {}
  
    def newFile(self, fileInfo, current=None):
        fileHash = fileInfo.hash
        if fileHash not in self.files:
            print(fileInfo.name)
            print(fileInfo.hash)
            self.files[fileHash] = fileInfo.name
               
               
class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    def hello(self, orchestrator, current=None):
        orchestrator.announce(orchestrator)


class OrchestratorI(TrawlNet.Orchestrator): #pylint: disable=R0903
    '''
    Orchestrator Module
    '''
    files = {}

    def __init__(self, files):
        self.files = files

    def set_params(self, downloader, topic_orch, prx):
        self.prx = prx
        orchestrators = topic_orch.getPublisher()
        self.downloader = downloader
        obj_subscritos = TrawlNet.OrchestratorEventPrx.uncheckedCast(orchestrators)
        obj_subscritos.hello(TrawlNet.OrchestratorPrx.checkedCast(self.prx))

    def downloadTask(self, url, current=None): # pylint: disable=C0103, W0613
        return self.downloader.addDownloadTask(url)

    def announce(self, orch, current=None):
        print("New", orch)

    def getFileList(self, current=None):
        songs = []
        for fileHash in self.files:
            fileInfo = TrawlNet.FileInfo()
            fileInfo.hash = fileHash
            fileInfo.name = self.files[fileHash]
            songs.append(fileInfo)
        return songs