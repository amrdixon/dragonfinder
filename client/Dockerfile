FROM python:3.7.5-slim-buster

LABEL author="Anna Dixon <anna@datafoss.com"

USER root

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    wget \ 
    python3 \
    ca-certificates \
    libgtk2.0-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

COPY main_application.py .

COPY api.py .

COPY client.py ./

RUN mkdir aws_creds

ADD /aws_creds/ ./aws_creds/

RUN mkdir config

ADD /config/ ./config/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python3 api.py