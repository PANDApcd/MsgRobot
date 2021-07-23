#! /bin/bash
NAME=MsgRobot
CONDA_PATH=/home/panda
set -e
rm -rf $CONDA_PATH/anaconda3/lib/python3.8/site-packages/$NAME
cp -rf $NAME $CONDA_PATH/anaconda3/lib/python3.8/site-packages/