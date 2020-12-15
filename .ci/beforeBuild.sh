#!/usr/bin/env bash

curl -L https://github.com/KOLANICH-libs/glossary.py/files/7643704/glossary.zip > glossary.zip;
unzip glossary.zip;
#sudo dpkg -i glossary_0.1.1_amd64.deb;
curl -L https://raw.githubusercontent.com/waltonseymour/glossary/master/MOCK_DATA.csv > tests/MOCK_DATA.csv;
bash -c "cd ./tests; glossary index ./MOCK_DATA.csv";
