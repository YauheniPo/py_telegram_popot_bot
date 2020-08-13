#!/bin/bash

git clone https://github.com/YauheniPo/py_telegram_popot_bot.git

cd py_telegram_popot_bot

docker build -t yauhenipo/popot_bot-test .

docker run yauhenipo/popot_bot-test
