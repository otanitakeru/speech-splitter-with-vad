import json
from pathlib import Path

from ATR503.formatter import convert_ATR503_format_from
from model.value_object.speech_position import SpeechPosition


def write_json_from_speech_positions(
    speech_positions: list[SpeechPosition], file_path: Path
):
    """
    発話区間のリストをJSONファイルに書き込む

    フォーマット:
    {
        "start_s": 発話開始時間（秒）
        "end_s": 発話終了時間（秒）
        "index": 発話番号
    }

    例)
    ```json
    [
        {
            "start_s": 0.0,  # 発話開始時間（秒）
            "end_s": 1.0,    # 発話終了時間（秒）
            "index": 1       # 発話番号
        },
    ]
    ```

    Args:
        speech_positions: 発話区間のリスト
        file_path: 出力ファイルのパス
    """
    result_json = []
    index = 1
    for speech_position in speech_positions:
        result_json.append(
            {
                "start_s": speech_position.start_s,
                "end_s": speech_position.end_s,
                "index": index,
            },
        )
        index += 1

    with open(file_path, "w") as f:
        json.dump(result_json, f, indent=2)


def write_text_from_speech_positions(
    wav_positions: list[SpeechPosition], file_path: Path, ATR_503_format: bool = False
):
    """
    発話区間のリストをテキストファイルに書き込む

    フォーマット:
    発話開始時間（秒）[タブ] 発話終了時間（秒）[タブ] 発話番号

    例)
    ```text
    0.0	1.0	1
    1.0	2.0	2
    ```

    Args:
        speech_positions: 発話区間のリスト
        file_path: 出力ファイルのパス
    """

    result_text = ""
    index = 1
    for wav_position in wav_positions:
        if ATR_503_format:
            result_text += f"{wav_position.start_s:7.2f}\t{wav_position.end_s:7.2f}\t{convert_ATR503_format_from(index)}\n"
        else:
            result_text += (
                f"{wav_position.start_s:7.2f}\t{wav_position.end_s:7.2f}\t{index}\n"
            )
        index += 1

    with open(file_path, "w") as f:
        f.write(result_text)


def get_speech_positions_from_file(file_path: Path) -> list[SpeechPosition]:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix == ".txt":
        with open(file_path, "r") as f:
            text = f.read()

        speech_positions = []
        for line in text.split("\n"):
            if line.strip() == "":
                continue

            start, end, _ = line.split("\t")
            speech_positions.append(
                SpeechPosition(start_s=float(start), end_s=float(end))
            )

        return speech_positions

    elif file_path.suffix == ".json":
        with open(file_path, "r") as f:
            json_data = json.load(f)

        speech_positions = []
        for data in json_data:
            speech_positions.append(
                SpeechPosition(start_s=data["start_s"], end_s=data["end_s"])
            )

        return speech_positions

    raise ValueError(f"Unsupported file type: {file_path.suffix}")
