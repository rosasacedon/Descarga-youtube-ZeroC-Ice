#!/bin/sh

./downloader.py --Ice.Config=server.config | tee proxy-downloader.out &

proxy=$(tail -1 proxy-downloader.out)

./orchestrator.py --Ice.Config=orchestrator.config "$proxy"



