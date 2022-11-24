#!/bin/bash

if [[ `id -u` -eq 0 ]]
then
    echo "Please, run as regular user"
    exit 1
fi


pip3 install get-mac mac-vendor-lookup

user=`whoami`
ipscanner_path=`find "/home/$user" -name ipscanner.py`
sudo ln -s $ipscanner_path "/usr/bin/ipscanner"
