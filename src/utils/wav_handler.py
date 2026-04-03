from pathlib import Path
from typing import Optional

import librosa
import numpy as np
import soundfile as sf

from utils.const import Const


def convert_to_mono(
    input_wav_data: np.ndarray, channel: Optional[int] = None
) -> np.ndarray:
    """
    音声データをモノラルに変換する

    Args:
        input_wav_data: 入力音声データ (shape: (samples,) or (samples, channels))
        channel: 抽出するチャンネルのインデックス (0-based)。
                 None の場合は全チャンネルの平均でモノラル化する。

    Returns:
        np.ndarray: モノラル化された音声データ (shape: (samples,))

    Raises:
        ValueError: channel が範囲外の場合
    """
    if input_wav_data.ndim == 1:
        return input_wav_data

    if channel is None:
        return input_wav_data.mean(axis=1)

    num_channels = input_wav_data.shape[1]
    if channel < 0 or channel >= num_channels:
        raise ValueError(
            f"チャンネルインデックス {channel} が範囲外です。有効範囲: 0 〜 {num_channels - 1}"
        )

    return input_wav_data[:, channel]


def resample_wav(
    input_wav_data: np.ndarray,
    sample_rate: int,
    target_sample_rate: int = Const.SAMPLE_RATE,
) -> np.ndarray:
    """
    音声ファイルのサンプリングレートの変更

    Args:
        input_wav_data: 入力音声データ
        sample_rate: 入力音声のサンプリングレート
        target_sample_rate: 変更後のサンプリングレート

    Returns:
        np.ndarray: サンプリングレート変更後の音声データ
    """

    resampled_data = librosa.resample(
        input_wav_data, orig_sr=sample_rate, target_sr=target_sample_rate
    )
    return resampled_data
