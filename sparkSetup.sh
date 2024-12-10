#/bin/bash

sudo mkdir /app
sudo apt-get install -y curl vim wget software-properties-common 
sudo apt-get isntall -y net-tools ca-certificates
sudo cp TrainingDataset.csv ValidationDataset.csv /app/
sudo apt install openjdk-8-jdk
sudo wget -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop2.7.tgz"
sudo mkdir -p /opt/spark
sudo tar -xvzf apache-spark.tgz -C /opt/spark --strip-components=1
sudo rm apache-spark.tgz

echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
echo "export PATH=\$SPARK_HOME/bin:\$PATH" >> ~/.bashrc
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc
echo "export PATH=$JAVA_HOME/bin:$PATH" >> ~/.bashrc
