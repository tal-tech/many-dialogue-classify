FROM ubuntu:18.04
ENV TZ Asia/Shanghai
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone &&\
    apt-get install -y --no-install-recommends tzdata  python3.6 python3-dev python3-tk \
    python3-pip python3-setuptools

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r /tmp/requirements.txt

COPY . /home/dolphin
WORKDIR /home/dolphin
ENV LANG C.UTF-8
ENV PYTHONIOENCODING utf-8
CMD exec gunicorn -w4 --keep-alive=16 -b0.0.0.0:5000 flask_app:app