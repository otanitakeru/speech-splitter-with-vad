from pathlib import Path

import librosa
import soundfile as sf

from utils.const.const import Const


def convert2mono(input_path: Path, output_path: Path):
    """
    音声ファイルのモノラル化

    Args:
        input_path: 入力ファイルのパス
        output_path: 出力ファイルのパス
    """

    data, sample_rate = sf.read(input_path)
    data = data.mean(axis=1)
    sf.write(output_path, data, sample_rate, format="WAV", subtype="PCM_16")


def resample_wav(
    input_path: Path, output_path: Path, target_sample_rate: int = Const.SAMPLE_RATE
):
    """
    音声ファイルのサンプリングレートの変更

    Args:
        input_path: 入力ファイルのパス
        output_path: 出力ファイルのパス
        target_sample_rate: 変更後のサンプリングレート
    """

    data, sample_rate = sf.read(input_path)
    resampled_wav = librosa.resample(
        data, orig_sr=sample_rate, target_sr=target_sample_rate
    )
    sf.write(
        output_path, resampled_wav, target_sample_rate, format="WAV", subtype="PCM_16"
    )


def convert_mono_16kHz_wav(wav_path: Path, output_dir: Path) -> Path:
    """
    音声ファイルのモノラル化と16kHzに変換
    (tmp.wav -> tmp.mono.wav -> tmp.16kHz.mono.wav)

    Args:
        wav_path: 入力ファイルのパス
        output_dir: 出力ディレクトリのパス

    Returns:
        Path: 出力ファイルのパス
    """

    mono_wav_path = wav_path.with_suffix(".mono.wav")
    convert2mono(wav_path, output_dir / mono_wav_path.name)

    resampled_mono_wav_path = wav_path.with_suffix(".mono.16kHz.wav")
    resample_wav(
        output_dir / mono_wav_path.name,
        output_dir / resampled_mono_wav_path.name,
        target_sample_rate=16000,
    )

    return output_dir / resampled_mono_wav_path.name


def write_wav(input_path: Path, output_path: Path, start_time: float, end_time: float):
    """
    音声ファイルの書き出し

    Args:
        input_path: 入力ファイルのパス
        output_path: 出力ファイルのパス
        start_time: 開始時間
        end_time: 終了時間
    """
    data, sample_rate = sf.read(input_path)
    data = data[int(start_time * sample_rate) : int(end_time * sample_rate)]
    sf.write(output_path, data, sample_rate, format="WAV")
