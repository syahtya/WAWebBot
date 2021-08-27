#!/bin/bash

sudo cp geckodriver /usr/bin/
sudo chmod 777 /usr/bin/geckodriver

chmod +x *

sudo mysql < init.sql

echo "JANGAN LUPA GAIS ATUR ENVIRONMENT CONFIG.JSON !!!"