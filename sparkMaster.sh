#/bin/bash

export SPARK_MASTER_PORT=7077
export SPARK_MASTER_WEBUI_PORT=8080
export SPARK_LOG_DIR=/opt/spark/logs
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

sudo mkdir -p $SPARK_LOG_DIR
sudo touch $SPARK_MASTER_LOG
sudo ln -sf /dev/stdout $SPARK_MASTER_LOG

export SPARK_MASTER_HOST=`hostname`

cd /opt/spark/bin &&
sudo ./spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT
