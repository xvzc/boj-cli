#!/bin/sh

mkdir -p ~/.boj-cli/
touch ~/.boj-cli/boj-token
touch ~/.boj-cli/boj-handle

curl https://raw.githubusercontent.com/xvzc/boj-cli/main/boj-submit.py > ~/.boj-cli/boj-submit.py
