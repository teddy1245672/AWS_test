#!/bin/bash
echo "Starting Django application..."
apt-get update
apt-get install -y python3-pip
pip3 install django whitenoise openpyxl djangorestframework
cd /home/ubuntu/aws_test
npm install
npm run build
python3 manage.py runserver 0.0.0.0:8000 &