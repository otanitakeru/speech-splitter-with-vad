# Speech Splitter with VAD

VAD（Voice Activity Detection）を使用して音声ファイルから発話区間を検出するPythonツールです。[Silero VAD](https://github.com/snakers4/silero-vad) を使用して高精度に発話区間を検出し、テキスト・JSON・グラフの3形式で結果を出力できます。

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd speech-splitter-with-vad
```

### 2. 仮想環境の作成と依存パッケージのインストール

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 使用方法

### シェルスクリプトで実行（推奨）

```bash
bash scripts/run_vad.sh <INPUT_WAV_PATH> <OUTPUT_DIR_PATH> <VAD_CONFIG_PATH>
```

例:

```bash
bash scripts/run_vad.sh \
    data/wav/test/test.wav \
    outputs/vad_results/test \
    config/test/vad.yaml
```

実行後、以下のディレクトリ構造で出力されます:

```
<OUTPUT_DIR_PATH>/
├── original/   # 入力ファイルと同ディレクトリのファイルをコピー
├── result/     # VAD結果ファイル
└── config/
    └── vad.yaml  # 使用したVAD設定のコピー
```

### Pythonスクリプトで直接実行

```bash
source venv/bin/activate
cd src
python run_vad.py \
    -i /path/to/audio.wav \
    --output_dir_path /path/to/output \
    --vad_config_path /path/to/vad.yaml \
    --write_text \
    --write_json \
    --write_plot
```

#### 引数一覧

| 引数                     | 型   | デフォルト | 説明                                       |
| ------------------------ | ---- | ---------- | ------------------------------------------ |
| `-i`, `--input_wav_path` | Path | -          | 入力音声ファイルのパス                     |
| `--output_dir_path`      | Path | -          | 出力先ディレクトリ                         |
| `--vad_config_path`      | Path | -          | VADパラメータのYAML設定ファイルパス        |
| `--channel`              | int  | `None`     | 使用するチャンネルのインデックス (0-based) |
| `--write_text`           | flag | `False`    | テキスト形式で結果を保存                   |
| `--write_json`           | flag | `False`    | JSON形式で結果を保存                       |
| `--write_plot`           | flag | `False`    | 波形プロット画像を保存                     |

`--channel` を省略すると全チャンネルの平均でモノラル化します。

## 出力ファイル

| ファイル名              | 説明                                                   |
| ----------------------- | ------------------------------------------------------ |
| `speech_positions.txt`  | `start_s \t end_s \t index` の形式で発話区間を列挙     |
| `speech_positions.json` | `[{"start_s": float, "end_s": float}, ...]` 形式のJSON |
| `vad_result.png`        | 音声波形に発話区間（赤ハイライト）を重ねたプロット     |

## VADパラメータのカスタマイズ

`src/config/config.py` の `SileroVadConfig` または YAMLファイルでパラメータを調整できます。

| パラメータ                          | デフォルト | 説明                                            |
| ----------------------------------- | ---------- | ----------------------------------------------- |
| `threshold`                         | `0.25`     | 発話判定の確率閾値                              |
| `neg_threshold`                     | `0.25`     | 発話→無音への遷移閾値                           |
| `min_speech_duration_ms`            | `200`      | 最小発話長（ms）。これ未満の区間は除外          |
| `max_speech_duration_s`             | `inf`      | 最大発話長（秒）。超過した場合は分割            |
| `min_silence_duration_ms`           | `250`      | Silero VAD が発話区間を分離する最小無音長（ms） |
| `speech_pad_ms`                     | `250`      | 発話区間の前後に追加するパディング（ms）        |
| `min_silence_duration_ms_after_vad` | `500`      | VAD後の後処理で隣接区間を結合する無音閾値（ms） |

YAMLファイルから読み込む例:

```python
from pathlib import Path
from config.config import SileroVadConfig

config = SileroVadConfig.load_from_yaml(Path("config.yaml"))
```

```yaml
# config.yaml
threshold: 0.3
min_silence_duration_ms: 300
speech_pad_ms: 100
```

## 参考

- [Silero VAD](https://github.com/snakers4/silero-vad)
