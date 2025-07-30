import shutil
from pathlib import Path

from model.value_object.vad_result import VadResultSpeechType
from service.plot.plot import plot_vad_analysis
from service.vad_result_handler import convert_json_to_text, get_json_from_vad_results
from service.wav_handler.wav_handler import convert2mono, resample_wav, write_wav
from vad.stereo_vad import StereoVad


def _convert_wav(wav_path: Path, output_dir: Path):
    mono_wav_path = wav_path.with_suffix(".mono.wav")
    resampled_mono_wav_path = wav_path.with_suffix(".16kHz.mono.wav")
    convert2mono(wav_path, output_dir / mono_wav_path.name)
    resample_wav(
        output_dir / mono_wav_path.name, output_dir / resampled_mono_wav_path.name
    )

    return output_dir / resampled_mono_wav_path.name


def _split_wav(wav_path: Path, output_dir: Path):
    if output_dir.exists():
        shutil.rmtree(output_dir)

    tmp_wav_dir = Path("data/tmp/wav")
    tmp_wav_dir.mkdir(parents=True, exist_ok=True)
    converted_wav_path = _convert_wav(wav_path, tmp_wav_dir)

    stereo_vad = StereoVad()
    vad_results = stereo_vad.execute_vad(converted_wav_path)
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

    plot_vad_analysis(
        converted_wav_path,
        vad_results,
        save_path=output_dir / "vad_analysis.png",
    )

    # wav_index = 1
    # for vad_result in vad_results:
    #     if vad_result.type == VadResultSpeechType.NON_SPEECH:
    #         continue

    #     write_wav(
    #         wav_path,
    #         output_dir / f"{wav_index}.wav",
    #         vad_result.get_start_time(),
    #         vad_result.get_end_time(),
    #     )
    #     wav_index += 1

    with open(output_dir / "wav_positions.json", "w") as f:
        vad_result_json = get_json_from_vad_results(vad_results, only_speech=True)
        f.write(vad_result_json)


def main():
    wav_path = Path("kikuchi.wav")
    output_dir = Path("data/output")
    _split_wav(wav_path, output_dir)
    convert_json_to_text(
        Path("data/output/wav_positions.json"),
        Path("data/output/wav_positions.txt"),
    )


if __name__ == "__main__":
    main()
