#!/usr/bin/bash
sudo apt-get install mysql-server mysql-client -y
sudo mysql --version
sudo service mysql start
sudo mysqladmin -u root create KOO -p
sudo mysqladmin -u root -p password k-oo1234
python table_init.py