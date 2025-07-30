from pathlib import Path

from service.vad_result_handler import convert_json_to_text


def main():
    convert_json_to_text(
        Path("data/output/wav_positions.json"),
        Path("data/output/wav_positions.txt"),
    )


if __name__ == "__main__":
    main()
