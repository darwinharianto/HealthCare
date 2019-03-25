#! /bin/sh

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt install libnfc5 libnfc-bin libnfc-examples -y
sudo apt-get remove gnome-terminal && sudo apt-get install gnome-terminal
sudo apt-get install python-pip
sudo apt-get  install  libusb-dev  libpcsclite-dev  i2c-tools  -y


sudo pip install nfcpy
sudo apt-get install libglib2.0-dev -y
sudo pip install bluepy


cd ~
wget http://dl.bintray.com/nfc-tools/sources/libnfc-1.7.1.tar.bz2
tar -xf libnfc-1.7.1.tar.bz2

cd libnfc-1.7.1
./configure --prefix=/usr --sysconfdir=/etc
make
sudo make install

sudo raspi-config

sudo mkdir   /etc/nfc
sudo nano   libnfc.conf

sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
