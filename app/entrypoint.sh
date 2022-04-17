#!/bin/bash

supervisord -c ./supervisord.conf

supervisorctl start all

tail -f .supervisord/supervisord.logfile
