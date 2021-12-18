- [Requires](#Requires)
- [Development](#Development)
- [Docker](#Docker)
- [Deployment](#Deployment)
- [APIs](#APIs)


This project builds a malware analysis platform

# Requires
*this sections contains common requirements for starting app in development mode and docker mode, we do not need this in deployment mode*

- docker-cuckoo

## docker-cuckoo

First, make sure vboxhostonlynic, vboxwebsrv, load-iptables running healthily
> see [mal_v2.service](stow/etc/systemd/system/mal_v2.service) for more details. 

Then, Start docker-cuckoo manually and make sure cuckoo listening on 8000

```shell
cd docker-cuckoo && docker-compose -f docker-compose.vbox.yml up -d 
```

if any error occurs, checks docker log for more detail

```shell
docker logs -f dockercuckoo_cuckoo_1
```

# Development 

## Pre-install

```shell
apt install nasm
pip3 install -r requirements.txt
```

## Adapt Conf 

the environment variable for start app is located in .env file

warning: it's a development-only file, ignored by .dockerignore

the env settings for docker are located in docker-compose.yaml

## Start App

Start redis, mongo, mongo-express, neo4j
```shell
docker-compose up -d redis mongo mongo-express neo4j
```

Start flask, celery and flower
```shell
supervisord -c ./supervisord.conf
supervisorctl start all    
```

logfile for mal_v2 is located in ./.supervisord/mal.logfile

# Docker

## Adapt Conf

set environment variable for docker-compose, just edit the docker-compose file!

## Start App
```shell
docker-compose up -d
```

# Deployment 

- TODO: install.sh

## Stow

```shell
stow -t / stow 
```

## Start App 

```shell
systemctl start mal_v2.service
```


# APIs

if you'd like to list all the available apis, run the following command

```
FLASK_APP=runserver:app flask routes
```

- upload file
    ```
    :curl -F '@file=upload.exe' 
    POST /api/v2/task/create     
    ```

- fetch report
    ```
    GET /api/v2/feature/report/get/${id}
    ```

- fetch database statiscs
    ```
    GET /api/v2/feature/get_api_distribution
    GET /api/v2/feature/dashboard
    ```

- fetch running status

    ```
    GET /api/v2/task/pending_list
    GET /api/v2/task/pending_cnt
    GET /api/v2/task/status/${id}
    GET /api/v2/task/running_list
    ```
