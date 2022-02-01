#!/bin/bash

set -e 

VBOX_USER="$(cat /etc/passwd|grep 1000|cut -d ':' -f 1)"

sed -i "s/User *=.*/User=$VBOX_USER/g" stow/etc/systemd/system/vboxwebsrv.service
