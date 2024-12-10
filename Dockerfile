FROM bitnami/spark:latest

RUN pip3 install pyspark pandas scikit-learn quinn
RUN apt-get install -y openjdk-8-jdk

COPY . /app
WORKDIR /app

EXPOSE 4040

ENTRYPOINT ["python3", "Predict.py"]
