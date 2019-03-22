#! /bin/sh

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt install libnfc5 libnfc-bin libnfc-examples -y
sudo apt-get remove gnome-terminal && sudo apt-get install gnome-terminal
sudo pip install nfcpy -y

sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
