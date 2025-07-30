# Speech Splitter with VAD

VAD（Voice Activity Detection）を使用して音声ファイルから発話区間を検出するPythonツールです。Silero VADモデルを使用して音声区間を検出し、視覚化と分析結果を提供します。

## 機能

- **Silero VAD**を使用した高精度な音声区間検出
- 音声ファイルの自動分割（VADベース）
- 音声区間の可視化
- 16kHzモノラル形式への自動変換
- 発話位置の詳細分析とテキスト出力
- VAD結果のグラフ表示

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd speech-splitter-with-vad
```

### 2. 依存関係のインストール

```bash
make setup
```

または手動でセットアップ：

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 使用方法

### 基本的な使用方法

```bash
# デフォルトのテストファイルで実行
make run

# または直接実行
source venv/bin/activate
python src/main.py [/path/to/your/audio/file]
```

## 出力ファイル

処理完了後、指定した出力ディレクトリ（デフォルト: `data/output`）に以下のファイルが生成されます：

- `wav_positions.txt`: 検出された音声区間の詳細情報
- `vad_analysis.png`: VAD結果の可視化グラフ

## Makeコマンド

```bash
make setup    # 環境セットアップ
make run      # デフォルト実行
make clean    # 一時ファイルクリーンアップ
```

## トラブルシューティング

### 音声ファイル形式

入力音声ファイルは自動的に16kHzモノラル形式に変換されます。対応形式：
- WAV, MP3, FLAC, M4A など（librosaが対応する形式）

### Silero VADについて

音声区間検出にSilero VADを使用しています：
- GitHub: https://github.com/snakers4/silero-vad
