#!/bin/sh
while true; do
    python3 -m sparkz.py;
    echo 'Restarting in 2 seconds...'
    sleep 2;
done
