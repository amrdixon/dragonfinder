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

COPY setup.py .

RUN mkdir classifier_client

ADD /classifier_client/ ./classifier_client/

RUN mkdir data_sample

ADD /data_sample/ ./data_sample/

RUN pip install --editable .

CMD ["/bin/bash"]