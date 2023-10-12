FROM python:3.10.12-slim-bullseye
WORKDIR /root/evotrack
ENV LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY . .
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free" > /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb https://security.debian.org/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list \
    && apt update \
    && apt install netcat python3-dev default-libmysqlclient-dev build-essential pkg-config -y \
    && pip3 install -i https://pypi.doubanio.com/simple -U pip setuptools \
    && pip3 install -i https://pypi.doubanio.com/simple -r requirements.txt \
    && chmod +x ./deploy_server.sh
ENTRYPOINT /bin/bash deploy_server.sh
