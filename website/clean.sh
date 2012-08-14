#!/bin/bash
for PIDFILE in `ls -1 run/*.pid`; do kill $(cat $PIDFILE); done
