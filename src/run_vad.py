import shutil
from pathlib import Path
from typing import Optional

from config.config import SileroVadConfig
from vad.silero_vad import SileroVad
from writer.plot_vad_result import plot_vad_result
from writer.speech_position_writer import (
    write_speech_position_to_json,
    write_speech_position_to_text,
)


def run_vad(wav_path: Path, vad_config: SileroVadConfig, channel: Optional[int] = None):
    silero_vad = SileroVad(config=vad_config)
    speech_positions = silero_vad.execute_vad(wav_path, channel=channel)
    return speech_positions


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_wav_path", type=Path, required=True)
    parser.add_argument(
        "--output_dir_path",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--vad_config_path",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--write_text",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--write_json",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--write_plot",
        action="store_true",
        default=False,
    )
    parser.add_argument("--channel", type=int, default=None)
    args = parser.parse_args()

    input_wav_path = Path(args.input_wav_path)
    output_dir_path = Path(args.output_dir_path)
    write_text = args.write_text
    write_json = args.write_json
    write_plot = args.write_plot
    if args.channel is not None:
        channel = int(args.channel)
    else:
        channel = None
    vad_config_path = Path(args.vad_config_path)

    vad_config = SileroVadConfig.load_from_yaml(vad_config_path)

    print("Running VAD...")
    speech_positions = run_vad(input_wav_path, channel=channel, vad_config=vad_config)

    print("Resulting speech positions:")

    for i in range(min(len(speech_positions), 10)):
        speech_position = speech_positions[i]
        duration = speech_position.end_s - speech_position.start_s

        print(f"{i+1}: ")
        print(
            f"{speech_position.start_s:7.2f}s - {speech_position.end_s:7.2f}s ({duration:6.2f}s)"
        )

    if len(speech_positions) > 10:
        print("...")

    if write_text:
        write_speech_position_to_text(
            speech_positions, output_dir_path / "speech_positions.txt"
        )
    if write_json:
        write_speech_position_to_json(
            speech_positions, output_dir_path / "speech_positions.json"
        )
    if write_plot:
        plot_vad_result(
            input_wav_path,
            speech_positions,
            output_dir_path / "vad_result.png",
            channel=channel,
        )
