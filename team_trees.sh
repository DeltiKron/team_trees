#!/bin/bash
source ~/anaconda3/bin/activate
conda activate sdc
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python $DIR/team_trees.py
