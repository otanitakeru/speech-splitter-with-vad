import json
from pathlib import Path

from model.value_object.vad_result import VadResult, VadResultSpeechType


def get_json_from_vad_results(
    vad_results: list[VadResult], only_speech: bool = False
) -> str:
    result_json = []
    index = 1
    for vad_result in vad_results:
        if only_speech and vad_result.type == VadResultSpeechType.NON_SPEECH:
            continue

        if only_speech:
            result_json.append(
                {
                    "start": vad_result.get_start_time(),
                    "end": vad_result.get_end_time(),
                    "index": index,
                },
            )
        else:
            result_json.append(
                {
                    "start": vad_result.get_start_time(),
                    "end": vad_result.get_end_time(),
                    "type": vad_result.type.value,
                    "index": index,
                },
            )
        index += 1

    return json.dumps(result_json, indent=2)


def get_text_from_speech_vad_results(vad_results: list[VadResult]) -> str:
    result_text = ""
    for vad_result in vad_results:
        if vad_result.type == VadResultSpeechType.SPEECH:
            result_text += (
                f"{vad_result.get_start_time()}\t{vad_result.get_end_time()}\n"
            )

    return result_text


def convert_json_to_text(json_path: Path, text_path: Path):
    with open(json_path, "r") as f:
        json_data = json.load(f)

    with open(text_path, "w") as f:
        index = 1
        for item in json_data:
            f.write(f"{item['start']}\t{item['end']}\t{index}\n")
            index += 1
