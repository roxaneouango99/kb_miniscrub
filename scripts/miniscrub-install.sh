#!/bin/bash

set -e
set -x


source /miniconda/etc/profile.d/conda.sh
conda activate
ln -s $(which pip) /kb/deployment/bin/pip3
export PATH=/kb/deployment/bin:$PATH
conda create -n "miniscrub" python=3.9.5
conda activate miniscrub
cd jgi-miniscrub
python3 nodocker-setup.py --nogpu
python --version