#!/usr/bin/bash

handler()
{
    kill -9 $PID
}

python3 $(dirname "$(realpath $0)")/main.py &
PID=$!

trap handler SIGINT
trap handler SIGTERM

wait $PID
