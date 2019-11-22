#!/bin/sh


./downloader.py --Ice.Config=server.config | tee proxy_downloader.out &

sleep 2

./orchestrator.py --Ice.Config=orchestrator.config "$(head -1 proxy_downloader.out)"




