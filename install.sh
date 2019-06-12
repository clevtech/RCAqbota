#!/usr/bin/env bash

sudo chmod 777 /RCAqbota/server.py
cp /RCAqbota/rc.service /lib/systemd/system/rc.service

sudo service rc start
sudo service rc enable