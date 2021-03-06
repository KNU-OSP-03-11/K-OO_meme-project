#!/bin/bash
# autorun file for autostarting webpage service

# check for update
echo "update start"
sudo apt-get update -y
sudo apt-get upgrade -y
echo "update complete!"

# install python environment
echo "python setup start"
if which python > /dev/null;then
    echo "python already installed"
    if which python3 > /dev/null;then
        echo "python3 already installed"
    else
        sudo apt install python3 -y
    fi
else
    sudo apt install python -y
    sudo apt install python3 -y
fi
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
sudo update-alternatives --config python << EOF
2
EOF

python --version
sudo apt install python3-pip -y
sudo apt-get install python3-venv -y
echo "python setup complete!"


# install java environment
echo "java setup start"
if which java > /dev/null; then
    echo "java already installed"
    if which javac > /dev/null; then
        echo "javac already installed"
    else 
        sudo apt install default-jdk -y
    fi
else
    sudo apt install default-jre -y
fi
java --version
javac --version
echo "java setup complete!"

# start python venv environment
echo "python venv start"
python -m venv pyvenv
source pyvenv/bin/activate
pip install -r requirements.txt
echo "python venv setup complete!"

# install mySQL
echo "mySQL setup start"
if which mysql > /dev/null; then
    echo "mySQL already installed"
    echo "password for mySQL required"
    echo "if you didn't setup password, please check 'readme_if_mysql_requests_password.txt'"
    chmod 755 db_clear.sh
    ./db_clear.sh
else
    sudo apt-get install mysql-server mysql-client -y
    sudo mysql --version
    sudo service mysql start
    echo "if 'password : ' appears, please press enter key"
    sudo mysqladmin -u root create KOO -p
    sudo mysql -u root -p << EOF
use mysql;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'k-oo1234';
USE KOO;
CREATE TABLE KOOtable
(
    id INT AUTO_INCREMENT KEY,
word VARCHAR(30) UNIQUE KEY,
title VARCHAR(1000),
link VARCHAR(1000),
useFreq INT,
searchFreq INT
);
CREATE TABLE LINKtable
(
    id INT AUTO_INCREMENT KEY,
    word VARCHAR(30) UNIQUE KEY,
    title1 VARCHAR(1000),
    link1 VARCHAR(1000),
    title2 VARCHAR(1000),
    link2 VARCHAR(1000),
    title3 VARCHAR(1000),
    link3 VARCHAR(1000),
    title4 VARCHAR(1000),
    link4 VARCHAR(1000),
    title5 VARCHAR(1000),
    link5 VARCHAR(1000)
);
\q
EOF
fi
echo "mySQL ready!"

# run program
echo "data crawling start"
# start crawling from title
python crawl_test.py
# add top 50 words with additional title
python crawl_links.py
echo "data crawling complete"

# flask web service run
echo "flask web service start"
python app.py



