#!/bin/bash

if [[ `id -u` -eq 0 ]]
then
    echo "Please, run as regular user"
    exit 1
fi


pip3 install get-mac mac-vendor-lookup

sudo ln -s "`pwd`/ipscanner.py" "/usr/bin/ipscanner"

