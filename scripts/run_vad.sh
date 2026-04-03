#!/usr/bin/env bash

set -euo pipefail

cd $(dirname $0)/..

INPUT_WAV_PATH=$1
OUTPUT_DIR_PATH=$2
VAD_CONFIG_PATH=$3

mkdir -p $OUTPUT_DIR_PATH
mkdir -p $OUTPUT_DIR_PATH/original
mkdir -p $OUTPUT_DIR_PATH/result
mkdir -p $OUTPUT_DIR_PATH/config

input_dir_path=$(dirname $INPUT_WAV_PATH)
cp -r $input_dir_path/* $OUTPUT_DIR_PATH/original
cp $VAD_CONFIG_PATH $OUTPUT_DIR_PATH/config/vad.yaml

python src/run_vad.py \
    -i $INPUT_WAV_PATH \
    --output_dir_path $OUTPUT_DIR_PATH/result \
    --vad_config_path $VAD_CONFIG_PATH \
    --write_text \
    --write_json \
    --write_plot
