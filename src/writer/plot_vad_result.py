from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

from utils.wav_handler import convert_to_mono
from vad.silero_vad import SpeechPosition


def plot_vad_result(
    wav_path: Path,
    speech_positions: list[SpeechPosition],
    save_path: Optional[Path] = None,
    channel: Optional[int] = None,
):
    """
    Args:
        wav_path (Path): 音声ファイルのパス
        vad_results (list[VadResult]): 音声区間の辞書のリスト
        save_path (Optional[Path]): プロットを保存するパス
        channel: Optional[int]: 音声チャンネルのインデックス (0-based)。
                                None の場合は全チャンネルの平均でモノラル化する。
    """
    audio_data, sample_rate = sf.read(wav_path)
    audio_data = convert_to_mono(audio_data, channel=channel)

    # VAD結果を音声データの時間軸に合わせて展開
    vad_array = np.zeros(len(audio_data))
    for speech_position in speech_positions:
        vad_array[
            int(speech_position.start_s * sample_rate) : int(
                speech_position.end_s * sample_rate
            )
        ] = 1

    time = np.arange(len(audio_data)) / sample_rate

    fig, ax = plt.subplots(figsize=(15, 5))

    if audio_data.ndim == 1:
        ax.plot(time, audio_data, color="steelblue", linewidth=0.6, label="Waveform")
    else:
        num_channels = audio_data.shape[1]
        for channel in range(num_channels):
            alpha = 0.85 if num_channels == 1 else 0.65
            ax.plot(
                time,
                audio_data[:, channel],
                linewidth=0.5,
                color=f"C{channel}",
                alpha=alpha,
                label=f"Channel {channel}",
            )

    y_min, y_max = audio_data.min(), audio_data.max()
    ax.fill_between(
        time,
        y_min,
        y_max,
        where=vad_array.astype(bool).tolist(),
        alpha=0.35,
        color="tomato",
        label="Speech (VAD)",
    )

    ax.set_xlim(0, time[-1])
    ax.set_title("Audio Waveform with VAD Result")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend(loc="upper right")
    ax.grid(True)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    else:
        plt.show()
