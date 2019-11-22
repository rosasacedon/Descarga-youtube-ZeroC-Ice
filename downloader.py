#!/usr/bin/env python3
# -*- coding: utf-8; -*-

'''
Downloader
'''

import sys
import os.path
import youtube_dl #pylint: disable=E0401
import Ice # pylint: disable=E0401,E0401
Ice.loadSlice('trawlnet.ice')
import TrawlNet # pylint: disable=E0401,C0413


class Downloader(TrawlNet.Downloader):  # pylint: disable=R0903
    '''
    Downloader
    '''
    def addDownloadTask(self, url, current=None): # pylint: disable=C0103, R0201, W0613
        '''
        Task
        '''
        print(url)
        return download_mp3(url)

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


class Servidor(Ice.Application): # pylint: disable=R0903
    '''
    Servidor
    '''

    def run(self, argv): # pylint: disable=W0613
        '''
        Iniciar servidor
        '''
        serv = Downloader()
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        dwn = adapter.add(serv, broker.stringToIdentity("dl"))
        print(dwn, flush=True)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

SERV = Servidor()
sys.exit(SERV.main(sys.argv))
