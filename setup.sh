#!/usr/bin/env bash

# ----- Aptitude Installs ----- #

# Update package list.
echo '-----> Updating package list...'
sudo apt-get update

# Install Python 3.
echo '-----> Installing Python 3...'
sudo apt-get install -y python3 python3-pip python3-venv

# Install Nginx.
echo '-----> Installing Nginx...'
sudo apt-get install -y nginx


# ----- Working Directory ----- #

WORKING_DIR=$(pwd)


# ----- Configure Nginx ----- #

echo '-----> Configuring Nginx...'

# Backup config file and then insert symlinks setting.
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx-backup.conf
sudo sed -i '/http {/a \ \ \ \ disable_symlinks off;' /etc/nginx/nginx.conf

# Create site file and copy to nginx directory.
MEDIA_DIR=$WORKING_DIR/media/
MEDIA_DIR="${MEDIA_DIR//\//\\/}"
sudo sed "s/\/home\/pi\/video-server\/media\//$MEDIA_DIR/g" nginx-config > /etc/nginx/sites-available/video-server

# Enable site file and reload config.
sudo ln -s /etc/nginx/sites-available/video-server /etc/nginx/sites-enabled/video-server
sudo nginx -s reload


# ----- Configure Virtual Environment ----- #

echo '-----> Creating Python virtual environment...'

# Create virtual environment.
pyvenv video-server-env

echo '-----> Installing Python dependencies...'

# Install dependencies.
$WORKING_DIR/video-server-env/bin/pip install -r requirements.txt


# ---- Configure Systemd ----- #

echo '-----> Configuring Systemd...'

# Replace paths to working directory.
WORKING_DIR_ESC="${WORKING_DIR//\//\\/}"
sed "s/\/home\/pi\/video-server/$WORKING_DIR_ESC/g" video-server.service > /etc/systemd/system/video-server.service

# Enable and start the service.
sudo systemctl enable /etc/systemd/system/video-server.service
sudo systemctl start video-server.service
