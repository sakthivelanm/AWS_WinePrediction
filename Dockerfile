FROM bitnami/spark:latest

RUN pip3 install pyspark pandas scikit-learn

COPY . /app
WORKDIR /app

EXPOSE 4040

ENTRYPOINT ["python3", "predict.py"]
