#!/bin/sh
#

echo "Downloading audio..."
./client.py "orchestrator" --download "$1" \
--Ice.Config=client.config

echo ""
echo "List request..."
./client.py --Ice.Config=client.config "orchestrator"

echo ""
echo "Init transfer..."
./client.py "orchestrator" --transfer "$2" \
--Ice.Config=client.config
