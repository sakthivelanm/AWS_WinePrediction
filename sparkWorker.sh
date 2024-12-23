#/bin/bash
export SPARK_MASTER_PORT=7077
export SPARK_MASTER_WEBUI_PORT=8080
export SPARK_LOG_DIR=/opt/spark/logs
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export SPARK_WORKER_WEBUI_PORT=8081
export SPARK_WORKER_PORT=7000
export SPARK_MASTER="spark://ip-172-31-22-218:7077"
export SPARK_LOCAL_IP=$(hostname -I | awk '{print $1}')

. "/opt/spark/bin/load-spark-env.sh"

sudo mkdir -p $SPARK_LOG_DIR
sudo touch $SPARK_WORkER_LOG
sudo ln -sf /dev/stdout $SPARK_WORKER_LOG
cd /opt/spark/bin
sudo ./spark-class org.apache.spark.deploy.worker.Worker --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER
