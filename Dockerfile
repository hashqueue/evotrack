FROM python:3.10
WORKDIR /root/evotrack
ENV LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY . .
RUN apt update \
    && apt install netcat -y \
    && pip3 install -U pip setuptools \
    && pip3 install -r requirements.txt \
    && chmod +x ./deploy_server.sh
ENTRYPOINT /bin/bash deploy_server.sh