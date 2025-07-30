import argparse
import shutil
from pathlib import Path

from model.value_object.vad_result import VadResultSpeechType
from service.speech_position_handler import (
    get_speech_position_from_vad_result,
    write_text_from_speech_positions,
)
from utils.const.const import Const
from utils.wav_handler.wav_handler import convert_mono_16kHz_wav
from vad.silero_vad import SileroVad
from visualizer.plot_vad_result import plot_vad_result
from visualizer.show_speech_position import show_speech_position

OUTPUT_DIR = Path("data/output")


def split_wav(wav_path: Path, output_dir: Path):
    """
    音声ファイルを分割する

    Args:
        wav_path: 入力ファイルのパス
        output_dir: 出力ディレクトリのパス
    """
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tmp_wav_dir = Path("data/tmp/wav")
    tmp_wav_dir.mkdir(parents=True, exist_ok=True)
    print("🚀 wavファイルを16kHzモノラルに変換しています...")
    converted_wav_path = convert_mono_16kHz_wav(wav_path, tmp_wav_dir)

    print("🚀 VADを実行しています...")
    silero_vad = SileroVad()
    vad_results = silero_vad.execute_vad(converted_wav_path)
    speech_positions = [
        get_speech_position_from_vad_result(vad_result, sample_rate=Const.SAMPLE_RATE)
        for vad_result in vad_results
        if vad_result.type == VadResultSpeechType.SPEECH
    ]
    show_speech_position(speech_positions)

    write_text_from_speech_positions(speech_positions, output_dir / "wav_positions.txt")

    plot_vad_result(
        converted_wav_path,
        vad_results,
        save_path=output_dir / "vad_analysis.png",
    )


def main():
    parser = argparse.ArgumentParser(description="音声ファイルを分割するツール")
    parser.add_argument("wav_path", type=Path, help="入力する音声ファイルのパス")
    parser.add_argument(
        "--output_dir", type=Path, default=OUTPUT_DIR, help="出力ディレクトリのパス"
    )
    args = parser.parse_args()

    wav_path: Path = args.wav_path
    output_dir: Path = args.output_dir
    split_wav(wav_path, output_dir)


if __name__ == "__main__":
    main()
