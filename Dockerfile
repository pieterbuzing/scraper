FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq dist-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        apt-utils \
        python3 \
        python3-dev \
        python3-mysqldb \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp* /var/tmp/* && \
    truncate -s 0 /var/log/*log

COPY ./algorithm /app/algorithm/
COPY ./scrapers /app/scrapers/
COPY ./sinks /app/sinks/
COPY ./settings.py /app/settings.py
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "./main.py"]
