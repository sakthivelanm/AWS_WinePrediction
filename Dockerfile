FROM bitnami/spark:latest

WORKDIR /app
COPY . /app

RUN pip3 install pyspark pandas scikit-learn

CMD ["python3", "predict.py"]
