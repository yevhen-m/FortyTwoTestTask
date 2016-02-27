#!/bin/sh

now=$(date +"%m_%d_%Y")
file="$now.dat"
python manage.py count_objects 2> $file
