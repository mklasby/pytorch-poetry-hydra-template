#!/bin/bash
cd ~
# Set up python and pip alias if required
# echo "alias python=python3" >> ~/.bashrc && echo "alias pip=pip3" >> ~/.bashrc

# Clone repo and cd into it
# Assumes ssh key already added to github.
git clone <<repo-url>>.git <<working-dir>>
cd <<working-dir>>
git checkout -t origin/main

# TODO: call from python
# # Create .env
# cp ./.env.template ./.env
# # Need to manually populate for now!

# Build venv
rm -rf ./.venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install poetry==<<poetry-version>>
poetry install -vvv

# Setup submodules
git submodule init && git submodule update
# Optionally build submodules here if required


# TODO: Do I need to populate this? Just use .env
# # Add wandb to env
# echo 'export WANDB_API_KEY=$WANDB_API_KEY' >> ~/.bashrc

# Copy data and unzip data, if required
sudo apt-get install unzip
cp -r ~/shared/ILSVRC ~/scratch/ILSVRC
cd ~/scratch/ILSVRC
unzip '*.zip'

# git conifg
git config --global user.name "<<name>>"
git config --global user.email "<<email>>"
echo "Build completed!"

