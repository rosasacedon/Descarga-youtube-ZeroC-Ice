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
        
