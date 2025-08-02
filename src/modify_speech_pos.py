import argparse
from pathlib import Path

from service.speech_pos_handler import (
    get_speech_positions_from_file,
    write_text_from_speech_positions,
)
from utils.time_handler import get_now_time_str
from visualizer.show_speech_position import show_speech_position

OUTPUT_DIR = Path("data/modify_speech_pos_output")


def modify_label(file_path: Path, output_dir: Path):
    speech_positions = get_speech_positions_from_file(file_path)
    show_speech_position(speech_positions)

    output_file_path = (
        output_dir
        / file_path.stem
        / get_now_time_str()
        / "modified_speech_positions.txt"
    )

    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    write_text_from_speech_positions(
        speech_positions, output_file_path, ATR_503_format=True
    )

    return speech_positions


def main():
    parser = argparse.ArgumentParser(description="音声ファイルを分割するツール")
    parser.add_argument("file_path", type=Path, help="入力するファイルのパス")
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=OUTPUT_DIR,
        help="出力するディレクトリのパス",
    )
    args = parser.parse_args()
    file_path: Path = args.file_path
    output_dir: Path = args.output_dir

    modify_label(file_path, output_dir)


if __name__ == "__main__":
    main()
