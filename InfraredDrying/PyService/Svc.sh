#!/bin/sh
ps -fe | grep python | grep ReadService1
if [ $? -ne 0 ]
then
echo "START RUN 1"
python ReadService1.py &
else
echo "ALready RUnning"
fi

ps -fe | grep python | grep ReadService2
if [ $? -ne 0 ]
then
echo "START RUN 2"
python ReadService2.py &
else
echo "ALready RUnning"
fi




