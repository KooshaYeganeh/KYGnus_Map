#!/usr/bin/bash



username=`users | cut -d" " -f1`


cd /home/$username/Apps/KYGnus_Map

source venv/bin/activate

python app.py

