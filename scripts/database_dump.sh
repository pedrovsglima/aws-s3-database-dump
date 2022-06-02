#!/bin/bash

sleep 20

date=$(date +'%F')
dateAndTime=$(date +'%F,%H:%M:%S')

mysqldump -hdatabase -uroot -pcesar FACULDADE > dumps/datadump.sql

echo "${dateAndTime},database dump completed" >> logs/"${date}".txt