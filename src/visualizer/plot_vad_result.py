from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from matplotlib.gridspec import GridSpec

from model.value_object.vad_result import VadResult


def plot_vad_result(
    wav_path: Path,
    vad_results: list[VadResult],
    save_path: Optional[Path] = None,
):
    """
    Args:
        wav_path (Path): 音声ファイルのパス
        vad_results (list[VadResult]): 音声区間の辞書のリスト
        save_path (Optional[Path]): プロットを保存するパス
    """
    audio_data, sample_rate = sf.read(wav_path)

    # VAD結果を音声データの時間軸に合わせて展開
    vad_array = np.zeros(len(audio_data))
    for result in vad_results:
        vad_array[result.start : result.end] = result.type.value

    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(2, 1, height_ratios=[1, 1])

    ax1 = fig.add_subplot(gs[0])
    time = np.arange(len(audio_data)) / sample_rate
    ax1.plot(time, audio_data)
    ax1.set_title("Audio Waveform")
    ax1.set_ylabel("Amplitude")
    ax1.set_xticklabels([])
    ax1.grid(True)

    ax2 = fig.add_subplot(gs[1])
    ax2.plot(time, vad_array)
    ax2.set_ylim(-0.5, 1.5)
    ax2.set_yticks([0, 1])
    ax2.set_title(f"Voice Activity Detection (VAD) Result")
    ax2.set_yticklabels(["Silent", "Speech"])
    ax2.set_xlabel("Time (s)")
    ax2.grid(True)

    xlim = (0, time[-1])
    ax1.set_xlim(xlim)
    ax2.set_xlim(xlim)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    else:
        plt.show()
