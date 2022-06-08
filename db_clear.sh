#!/bin/bash

sudo mysql -u root -p << EOF
DROP DATABASE KOO;
CREATE DATABASE KOO;
use KOO;
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
echo "mysql DB cleared"
