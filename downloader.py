#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Downloader
'''

import sys
import hashlib
import os.path
import youtube_dl
import Ice # pylint: disable=E0401
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413


class DownloaderI(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    DownloaderI
    '''
    publisher = None

    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        addDownloadTask
        '''
        descarga = download_mp3(url)
        if not descarga:
            raise TrawlNet.DownloadError("Error en la descarga")

        file_info = TrawlNet.FileInfo()
        file_info.name = os.path.basename(descarga)
        file_info.hash = compute_hash(file_info.name)

        if self.publisher is not None:
            self.publisher.newFile(file_info)
            
        return file_info

class Server(Ice.Application): # pylint: disable=R0903
    '''
    Server
    '''
    def run(self, argv): # pylint: disable=W0613,W0221
        '''
        Run
        '''
        key = 'IceStorm.TopicManager.Proxy'
        topic_name = "UpdateEvents"
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            return None

        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(proxy) # pylint: disable=E1101

        if not topic_mgr:
            return 2

        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic: # pylint: disable=E1101
            topic = topic_mgr.create(topic_name)

        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")

        downloader = DownloaderI()
        publisher = topic.getPublisher()

        downloader.publisher = TrawlNet.UpdateEventPrx.uncheckedCast(publisher)
        proxy = adapter.addWithUUID(downloader)
        print(proxy, flush=True)
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
        debug method
        '''
        pass

    def warning(self, msg):
        '''
        warning method
        '''
        pass

    def error(self, msg):
        '''
        error method
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


def download_mp3(url, destination='./'):
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

def compute_hash(filename):
    '''
    Compute
    '''
    file_hash = hashlib.sha256()
    with open(filename, "rb") as new_file:
        for chunk in iter(lambda: new_file.read(4096), b''):
            file_hash.update(chunk)
    return file_hash.hexdigest()



SERVER = Server()
sys.exit(SERVER.main(sys.argv))