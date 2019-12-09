#!/usr/bin/env python3
# -*- coding: utf-8; -*-

'''
Downloader
'''

import sys
import os.path
import hashlib
import youtube_dl #pylint: disable=E0401
import Ice # pylint: disable=E0401,E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413


class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    Downloader
    '''
     publisher = None

    def __init__(self, topic):
        self.topic = topic
    
    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        Task
        '''
        fileSystem = download_mp3(url)
        fileInfo = TrawlNet.FileInfo()
        fileInfo.name = os.path.basename(fileSystem)
        fileInfo.hash = hash_this(fileInfo.name)
        orchestrators = self.topic.getPublisher()
        object_orchestrator_event = TrawlNet.UpdateEventPrx.uncheckedCast(orchestrators)
        object_orchestrator_event.newFile(fileInfo)
        return fileInfo

class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server instance
    '''
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            return None

        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv): # pylint: disable=W0613
        '''
        Run Server
        '''
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            return 2

        topic_name = "UpdateEvents"
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        servant = DownloaderI(topic)
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        prox = adapter.add(servant, broker.stringToIdentity("downloader"))
        print(prox, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

class NullLogger:
    '''
    NullLogger
    '''
    def debug(self, msg):
        '''
        Debug
        '''
        pass

    def warning(self, msg):
        '''
        Warning
        '''
        pass

    def error(self, msg):
        '''
        Error
        '''
        pass


_YOUTUBEDL_OPTS_ = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}


def download_mp3(url, destination='./music/'):
    '''
    Synchronous download from YouTube
    '''
    options = {}
    task_status = {}

    def progress_hook(status):
        '''
        progress hook
        '''
        task_status.update(status)
    options.update(_YOUTUBEDL_OPTS_)
    options['progress_hooks'] = [progress_hook]
    options['outtmpl'] = os.path.join(destination, '%(title)s.%(ext)s')

    with youtube_dl.YoutubeDL(options) as youtube:
        youtube.download([url])
    filename = task_status['filename']
    filename = filename[:filename.rindex('.') + 1]
    return filename + options['postprocessors'][0]['preferredcodec']

def hash_this(filename):
    fileHash = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b''):
            fileHash.update(chunk)
    return fileHash.hexdigest()


SERVER_DOWN = Server()
sys.exit(SERVER_DOWN.main(sys.argv))
