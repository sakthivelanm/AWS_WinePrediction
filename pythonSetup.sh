#/bin/bash

sudo apt install libssl-dev -y
sudo apt install python3 python3-pip python3-venv -y
source ~/myenv/bin/activate
sudo chown -R ubuntu:ubuntu ~/myenv
pip install dumpy pandas pyspark quinn findspark
