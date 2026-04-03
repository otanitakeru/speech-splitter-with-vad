import json
from pathlib import Path

from vad.silero_vad import SpeechPosition


def write_speech_position_to_text(
    speech_positions: list[SpeechPosition], output_path: Path
) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        for i, speech_position in enumerate(speech_positions):
            f.write(
                f"{speech_position.start_s:7.2f}\t{speech_position.end_s:7.2f}\t{i+1}\n"
            )


def write_speech_position_to_json(
    speech_positions: list[SpeechPosition], output_path: Path
) -> None:

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            [speech_position.to_dict() for speech_position in speech_positions],
            f,
            indent=4,
            ensure_ascii=False,
        )
