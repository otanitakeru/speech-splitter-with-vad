#!/bin/bash

set -euo pipefail

# プロジェクトのルートディレクトリを取得
project_root_dir=$(cd $(dirname $0)/.. && pwd)

WAV_PATH=assets/wav/original/test.wav
OUTPUT_DIR=data/output

./venv/bin/python src/main.py $WAV_PATH --output_dir $OUTPUT_DIR
