#!/bin/bash

clear

echo "Cloning your repository..."
git clone https://github.com/MhdiTaheri/SNIChecker.git

clear

cd SNIChecker

pip install -r requirements.txt

clear

echo "Running the Python script..."
python3 sni_checker.py
