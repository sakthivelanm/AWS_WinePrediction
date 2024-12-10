FROM bitnami/spark:latest

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install pyspark pandas scikit-learn

COPY . /app
WORKDIR /app

EXPOSE 4040

CMD ["python3", "predict.py"]
