#!/usr/bin/env bash

# ----- Aptitude Installs ----- #

# Install python if not present.
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# Install Nginx.
sudo apt-get install -y nginx


# ----- Working Directory ----- #

WORKING_DIR=$(pwd)


# ----- Configure Nginx ----- #

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

# Create virtual environment.
pyvenv video-server-env

# Install dependencies.
$WORKING_DIR/video-server-env/bin/pip install -r requirements.txt


# ---- Configure Systemd ----- #

# Replace paths to working directory.
WORKING_DIR_ESC="${WORKING_DIR//\//\\/}"
sed "s/\/home\/pi\/video-server/$WORKING_DIR_ESC/g" video-server.service > /etc/systemd/system/video-server.service

# Enable and start the service.
sudo systemctl enable /etc/systemd/system/video-server.service
sudo systemctl start video-server.service
