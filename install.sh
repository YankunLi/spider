#!/bin/bash

set -x

CURRENT_PATH=`pwd`

CONFIG_PATH='/etc/spider/'
CONFIG_FILE='spider.conf'

#check config file resource
if [ ! -f "$CURRENT_PATH/etc/spider/spider.conf.sample" ]; then
    echo "don't found config file"
    exit 1
fi

#config spider 
if [ ! -d "$CONFIG_PATH" ]; then
    mkdir -p $CONFIG_PATH
fi

if [ ! -f "$CONFIG_PATH/$CONFIG_FILE" ]; then
   cp $CURRENT_PATH/etc/spider/spider.conf.sample $CONFIG_PATH/$CONFIG_FILE
fi

#install spider
python setup.py install
set +x
if [ 0 != $? ]; then
   echo 'ERROR: install error'
else
   echo 'congratulation, install successful'
fi

