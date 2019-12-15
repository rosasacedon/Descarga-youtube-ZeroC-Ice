 #!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import sys
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413

UPDATE_EVENTS = "UpdateEvents"
ORCHESTRATOR_SYNC = "OrchestratorSync"

class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    '''
    OrchestratorEventI
    '''
    orchestrator = None

    def hello(self, orchest, current=None):
        '''
        Hola!
        '''
        if self.orchestrator:
            self.orchestrator.saludar_orchestrator(orchest)

class FileUpdatesEventI(TrawlNet.UpdateEvent):
    '''
    FileUpdatesEventI
    '''
    orchestrator = None

    def newFile(self, file_info, current=None):
        '''
        newFile
        '''
        if self.orchestrator:
            file_hash = file_info.hash
            if file_hash not in self.orchestrator.files:
                self.orchestrator.files[file_hash] = file_info.name


class OrchestratorI(TrawlNet.Orchestrator):
    '''
    OrchestratorI
    '''
    orchestrator = None

    def downloadTask(self, url, current=None):
        '''
        downloadTask
        '''
        if self.orchestrator:
            return self.orchestrator.enviar_downloadTask(url)

    def getFileList(self, current=None):
        '''
        getFileList
        '''
        file_list = []
        if self.orchestrator:
            return self.orchestrator.get_list()
        return file_list

    def announce(self, other, current=None):
        '''
        Announce orchestrator
        '''
        if self.orchestrator:
            self.orchestrator.nuevo(other)

class GestionOrchestrators():
    files = {}
    orchestrators = {}
    qos = {}
    adapter = None
    downloader = None

    def __init__(self, broker, downloader_proxy, topic_mgr):
        self.set_all_params(broker, downloader_proxy, topic_mgr)
        self.run_orchestrator()
    
    def set_all_params(self, broker, downloader_proxy, topic_mgr):
        ''' set_all_params '''
        self.files = {}
        self.orchestrators = {}
        self.qos = {}
        self.adapter = broker.createObjectAdapter("OrchestratorAdapter")
        self.downloader = TrawlNet.DownloaderPrx.checkedCast(broker.stringToProxy(downloader_proxy))
       
        self.sync_topic = create_topic_by_name(ORCHESTRATOR_SYNC, topic_mgr)
        self.servant = OrchestratorI()
        self.servant.orchestrator = self
        self.proxy = self.adapter.addWithUUID(self.servant)

        self.subscriber = OrchestratorEventI()
        self.subscriber.orchestrator = self
        self.subscriber_proxy = self.adapter.addWithUUID(self.subscriber)
        self.sync_topic.subscribeAndGetPublisher(self.qos, self.subscriber_proxy)
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.sync_topic.getPublisher())

        self.file_updates = FileUpdatesEventI()
        self.file_updates.orchestrator = self
        self.file_topic = create_topic_by_name(UPDATE_EVENTS, topic_mgr)
        self.file_updates_proxy = self.adapter.addWithUUID(self.file_updates)
        self.file_topic.subscribeAndGetPublisher(self.qos, self.file_updates_proxy)


    def enviar_downloadTask(self, url):
        '''
        send_downloadTask
        '''
        return self.downloader.addDownloadTask(url)

    def saludar_orchestrator(self, orchestrator):
        '''
        saludar 
        '''
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("Hola soy el nuevo %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator
        orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.proxy))


    def nuevo(self, orchestrator):
        if orchestrator.ice_toString() in self.orchestrators:
            return
        print("Hola soy el viejo %s" % orchestrator.ice_toString())
        self.orchestrators[orchestrator.ice_toString()] = orchestrator

    def get_list(self):
        '''
        obtener lista
        '''
        fileList = []
        for fileHash in self.files:
            fileInfo = TrawlNet.FileInfo()
            fileInfo.hash = fileHash
            fileInfo.name = self.files[fileHash]
            fileList.append(fileInfo)
        return fileList

    def run_orchestrator(self):
        ''' Iniciar orchestrator '''
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.proxy))


    def __str__(self):
        ''' str '''
        return str(self.subscriber_proxy)

class Server(Ice.Application):  #pylint: disable=R0903
    '''
    Servidor
    '''

    def run(self, argv):
        '''
        Iniciar servidor
        '''
        broker = self.communicator()
        topic_mgr = get_topic_manager(broker)
        if not topic_mgr:
            return 2
        GestionOrchestrators(broker, argv[1], topic_mgr)
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

def create_topic_by_name(topic_name, topic_mgr):
    try:
        return topic_mgr.retrieve(topic_name)
    except IceStorm.NoSuchTopic: # pylint: disable=E1101
        return topic_mgr.create(topic_name)


def get_topic_manager(broker):
    key = 'IceStorm.TopicManager.Proxy'
    proxy = broker.propertyToProxy(key)
    if proxy is None:
        return None
    return IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101

ORCHESTRATOR = Server()
sys.exit(ORCHESTRATOR.main(sys.argv))