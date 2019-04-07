#!/bin/sh

sudo apt-get install -y nodejs npm
sudo apt autoremove -y
sudo npm cache clean
sudo npm install -y n -g
sudo n stable
npm -v

