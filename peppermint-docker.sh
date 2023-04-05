#!/bin/bash

# Install Docker on Ubuntu Server
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER

# Install Docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Set up Peppermint Ticket System
mkdir peppermint-ticket-system
cd peppermint-ticket-system
cat <<EOF > docker-compose.yml
version: '3'
services:
  web:
    image: peppermintnetworks/ticketsystem:latest
    ports:
      - "80:80"
    environment:
      - MYSQL_HOST=database
      - MYSQL_PORT=3306
      - MYSQL_DATABASE=ticketsystem
      - MYSQL_USER=ticketsystem
      - MYSQL_PASSWORD=password
    depends_on:
      - database
  database:
    image: mysql:5.7
    environment:
      - MYSQL_DATABASE=ticketsystem
      - MYSQL_USER=ticketsystem
      - MYSQL_PASSWORD=password
      - MYSQL_ROOT_PASSWORD=rootpassword
    volumes:
      - db-data:/var/lib/mysql
volumes:
  db-data:
EOF

# Start the Peppermint Ticket System
sudo docker-compose up -d
