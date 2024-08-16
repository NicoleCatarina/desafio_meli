FROM python:3-alpine

RUN pip install scapy mysql-connector-python

COPY analisador_trafego.py /app/analisador_trafego.py
COPY db.py /app/db.py
COPY analisador_pacotes.py /app/analisador_pacotes.py

WORKDIR /app

ENTRYPOINT ["python", "analisador_trafego.py"]