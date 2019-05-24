#!/bin/sh
cp -R -u -p config.json.gen config.json
sparkz () {
    if python3 -m sparkz; then
        clear
        #echo 'Restarting in 2 seconds...'
        echo 'Restarting...'
        clear
        #sleep 2;
        sparkz
     else
        echo 'An error was thrown, shutting down.'
    fi
}

sparkz