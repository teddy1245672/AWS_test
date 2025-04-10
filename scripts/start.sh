#!/bin/bash
echo "Starting Django application..."
apt-get update
apt-get install -y python3-pip
pip3 install django whitenoise openpyxl djangorestframework
#curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
#source ~/.nvm/nvm.sh
#nvm install 12.16.1
#npm install vue@2.5.17
cd /home/ubuntu/AWS_test
#sudo npm install
#npm run build
nohup python3 manage.py runserver 0.0.0.0:8000 &
