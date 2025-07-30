import shutil
from pathlib import Path

from model.value_object.vad_result import VadResultSpeechType
from plot.plot_vad_result import plot_vad_result
from service.vad_result_handler import convert_json_to_text, get_json_from_vad_results
from utils.wav_handler.wav_handler import convert_mono_16kHz_wav
from vad.silero_vad import SileroVad


def _split_wav(wav_path: Path, output_dir: Path):
    if output_dir.exists():
        shutil.rmtree(output_dir)

    tmp_wav_dir = Path("data/tmp/wav")
    tmp_wav_dir.mkdir(parents=True, exist_ok=True)
    converted_wav_path = convert_mono_16kHz_wav(wav_path, tmp_wav_dir)

    silero_vad = SileroVad()
    vad_results = silero_vad.execute_vad(converted_wav_path)
    print(
        "有声区間の数: ",
        len(
            [
                vad_result
                for vad_result in vad_results
                if vad_result.type == VadResultSpeechType.SPEECH
            ]
        ),
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    plot_vad_result(
        converted_wav_path,
        vad_results,
        save_path=output_dir / "vad_analysis.png",
    )

    with open(output_dir / "wav_positions.json", "w") as f:
        vad_result_json = get_json_from_vad_results(vad_results, only_speech=True)
        f.write(vad_result_json)


def main():
    wav_path = Path("assets/wav/original/kikuchi.wav")
    output_dir = Path("data/output")
    _split_wav(wav_path, output_dir)
    convert_json_to_text(
        Path("data/output/wav_positions.json"),
        Path("data/output/wav_positions.txt"),
    )


if __name__ == "__main__":
    main()
