#/bin/bash

sudo apt update && sudo apt upgrade -y
sudo mkdir /app
sudo cp TrainingDataset.csv ValidationDataset.csv /app/
sudo apt install openjdk-11-jdk -y
sudo wget -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop2.7.tgz"
sudo mkdir -p /opt/spark
sudo tar -xvzf apache-spark.tgz -C /opt/spark --strip-components=1
sudo rm apache-spark.tgz

sudo export SPARK_HOME=/opt/spark >> ~/.bashrc
sudo export PATH=\$SPARK_HOME/bin:\$PATH >> ~/.bashrc
sudo source ~/.bashrc
