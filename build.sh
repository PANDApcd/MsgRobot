#! /bin/bash
NAME=MsgRobot
set -e
rm -rf $CONDA_PREFIX/lib/python3.9/site-packages/$NAME
cp -rf $NAME $CONDA_PREFIX/lib/python3.9/site-packages/