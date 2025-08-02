import argparse
from pathlib import Path

from service.speech_pos_handler import write_text_from_speech_positions
from utils.time_handler import get_now_time_str
from utils.wav_handler import convert_mono_16kHz_wav
from vad.silero_vad import SileroVad
from visualizer.plot_vad_result import plot_vad_result
from visualizer.show_speech_position import show_speech_position

OUTPUT_DIR = Path("data/output")


def split_wav(wav_path: Path, output_dir: Path, plot_analysis: bool):
    """
    音声ファイルを分割する

    Args:
        wav_path: 入力ファイルのパス
        output_dir: 出力ディレクトリのパス
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    tmp_wav_dir = Path("data/tmp/wav")
    tmp_wav_dir.mkdir(parents=True, exist_ok=True)
    print("🚀 wavファイルを16kHzモノラルに変換しています...")
    converted_wav_path = convert_mono_16kHz_wav(wav_path, tmp_wav_dir)

    print("🚀 VADを実行しています...")
    silero_vad = SileroVad()
    speech_positions = silero_vad.execute_vad(converted_wav_path)
    show_speech_position(speech_positions)

    write_text_from_speech_positions(
        speech_positions, output_dir / "speech_positions.txt"
    )

    if plot_analysis:
        plot_vad_result(
            converted_wav_path,
            speech_positions,
            save_path=output_dir / "vad_analysis.png",
        )


def main():
    parser = argparse.ArgumentParser(description="音声ファイルを分割するツール")
    parser.add_argument("wav_path", type=Path, help="入力する音声ファイルのパス")
    parser.add_argument(
        "--output_dir", type=Path, default=OUTPUT_DIR, help="出力ディレクトリのパス"
    )
    parser.add_argument(
        "--plot_analysis",
        action="store_true",
        help="VADの結果をプロットする",
    )
    args = parser.parse_args()

    wav_path: Path = args.wav_path
    output_dir: Path = args.output_dir / wav_path.stem / get_now_time_str()
    plot_analysis: bool = args.plot_analysis
    output_dir.mkdir(parents=True, exist_ok=True)
    split_wav(wav_path, output_dir, plot_analysis)


if __name__ == "__main__":
    main()
