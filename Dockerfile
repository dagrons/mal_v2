FROM python:3.7.10-stretch

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update && \
    apt-get install -y nasm 

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install torch torchvision
    
RUN pip install -r /tmp/requirements.txt

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 FLASK_ENV=development

EXPOSE 5000 5656

WORKDIR /app

VOLUME [ "/app" ]

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh" ]