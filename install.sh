#!/bin/bash

clear

echo "Updating and upgrading the server..."
sudo apt update && sudo apt upgrade -y

echo "Cloning your repository..."
git clone https://github.com/MhdiTaheri/SNIChecker.git

cd SNIChecker

pip install -r requirements.txt

echo "Running the Python script..."
python3 sni_checker.py
