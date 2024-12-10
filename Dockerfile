FROM fokkodriesprong/docker-pyspark

USER root
RUN java -version
RUN pip3 install pyspark pandas scikit-learn quinn

COPY . /app
WORKDIR /app

EXPOSE 4040

ENTRYPOINT ["python3", "Predict.py"]
