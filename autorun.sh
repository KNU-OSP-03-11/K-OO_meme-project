#!/bin/bash
# autorun file for autostarting webpage service

# check for update
sudo apt-get update -y
sudo apt-get upgrade -y
echo "update complete!"

# install python environment
sudo apt install python -y
sudo apt install python3 -y
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
sudo update-alternatives --config python
2
python --version
sudo apt install python3-pip
sudo apt-get install python3-venv
echo "python setup complete!"

# install java environment
sudo apt install default-jre -y
sudo apt install default-jdk -y
java --version
javac --version
echo "java setup complete!"

# start python venv environment
python -m venv pyvenv
source pyvenv/bin/activate
pip install web_crawler/requirements.txt



