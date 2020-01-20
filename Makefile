#!/usr/bin/make -f
# -*- mode:makefile -*-

all:


clean:
	$(RM) -r /tmp/db
	$(RM) -r /tmp/YoutubeDownloaderApp

run: clean
	$(MAKE) app-workspace
	$(MAKE) run-registry-node &
	sleep 2
	$(MAKE) run-downloads-node &
	sleep 2
	$(MAKE) run-orchestrator-node

run-client-download:
	echo "Descargando archivo..."
	./client.py --Ice.Config=client.config "orchestrator" "--download" $(url)

run-client-transfer:
	echo "Transfiriendo..."
	./client.py --Ice.Config=client.config "orchestrator" "--transfer" "$(nombre)"


run-client-list:
	./client.py --Ice.Config=client.config "orchestrator"

run-registry-node: /tmp/db/registry /tmp/db/registry-node/servers 
	icegridnode --Ice.Config=registry-node.config

run-orchestrator-node: /tmp/db/orchestrator-node/servers 
	icegridnode --Ice.Config=orchestrator-node.config

run-downloads-node: /tmp/db/downloads-node/servers 
	icegridnode --Ice.Config=downloads-node.config

app-workspace: /tmp/YoutubeDownloaderApp
	cp trawlnet.ice orchestrator.py downloader_factory.py \
	transfer_factory.py utils.py /tmp/YoutubeDownloaderApp
	icepatch2calc /tmp/YoutubeDownloaderApp

/tmp/%:
	mkdir -p $@
