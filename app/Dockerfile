FROM python:3.7.10-stretch

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 FLASK_ENV=development

EXPOSE 5000 5656

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh" ]
