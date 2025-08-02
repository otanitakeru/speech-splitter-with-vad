#!/bin/bash

set -euo pipefail

# プロジェクトのルートディレクトリを取得
project_root_dir=$(cd $(dirname $0)/.. && pwd)

SPEECH_POS_PATH=data/speech_pos/test.txt

./venv/bin/python src/modify_speech_pos.py $SPEECH_POS_PATH
