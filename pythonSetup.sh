#/bin/bash

sudo apt install libssl-dev -y
sudo apt install python3 python3-pip python3-venv -y
python3 -m venv ~/myenv
source ~/myenv/bin/activate
sudo chown -R ubuntu:ubuntu ~/myenv
pip install numpy pandas pyspark quinn findspark
