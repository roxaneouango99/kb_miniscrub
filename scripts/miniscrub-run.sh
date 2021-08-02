#!/bin/bash

set -x
set -e

source /miniconda/etc/profile.d/conda.sh
conda activate miniscrub
cd /kb/module/jgi-miniscrub
eval $MINISCRUB_COMMAND