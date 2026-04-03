from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import soundfile as sf
import torch
from silero_vad import get_speech_timestamps, load_silero_vad
from torch import Tensor

from config.config import SileroVadConfig
from utils.const import Const
from utils.wav_handler import convert_to_mono, resample_wav


@dataclass
class SpeechPosition:
    start_s: float
    end_s: float

    def __str__(self):
        return f"SpeechPosition(start={self.start_s}, end={self.end_s})"

    def __repr__(self):
        return f"SpeechPosition(start={self.start_s}, end={self.end_s})"

    def to_dict(self):
        return {
            "start_s": self.start_s,
            "end_s": self.end_s,
        }


class SileroVad:
    def __init__(self, config: SileroVadConfig = SileroVadConfig()):
        self.config = config
        self.model = load_silero_vad(onnx=True)

    def execute_vad(
        self, wav_path: Path, channel: Optional[int] = None
    ) -> list[SpeechPosition]:
        """
        Args:
            wav_path: 音声ファイルのパス
            channel: 音声チャンネルのインデックス (0-based)。
                     None の場合は全チャンネルの平均でモノラル化する。
        Returns:
            list[VadResult]: 音声区間のリスト
        """

        sample_rate = Const.SAMPLE_RATE
        wav_data, original_sample_rate = sf.read(wav_path)
        wav_data = convert_to_mono(wav_data, channel=channel)
        wav_data = resample_wav(wav_data, original_sample_rate, sample_rate)

        speech_positions = self._execute_silero_vad(
            torch.from_numpy(wav_data).float(), sample_rate
        )

        concatinated_speech_positions = self._concatinate_speech_vad_results(
            speech_positions,
            min_silence_duration_ms_after_vad=self.config.min_silence_duration_ms_after_vad,
        )

        return concatinated_speech_positions

    def _execute_silero_vad(
        self, wav_data: Tensor, sample_rate: int
    ) -> list[SpeechPosition]:
        """
        Args:
            wav_path: 音声ファイルのパス

        Returns:
            list[SpeechPosition]: 音声区間のリスト(発話区間のみ)
        """

        speech_timestamps = get_speech_timestamps(
            wav_data,
            self.model,
            threshold=self.config.threshold,
            min_speech_duration_ms=self.config.min_speech_duration_ms,
            max_speech_duration_s=self.config.max_speech_duration_s,
            min_silence_duration_ms=self.config.min_silence_duration_ms,
            speech_pad_ms=self.config.speech_pad_ms,
            neg_threshold=self.config.neg_threshold,
        )

        return_results: list[SpeechPosition] = []

        for timestamp in speech_timestamps:
            start_s = timestamp["start"] / sample_rate
            end_s = min(timestamp["end"] / sample_rate, len(wav_data) / sample_rate)

            return_results.append(
                SpeechPosition(
                    start_s=start_s,
                    end_s=end_s,
                )
            )

        return return_results

    def _concatinate_speech_vad_results(
        self,
        speech_positions: list[SpeechPosition],
        min_silence_duration_ms_after_vad: int = 0,
    ) -> list[SpeechPosition]:
        """
        Args:
            vad_results: VAD結果のリスト

        Returns:
            list[SpeechPosition]: 結合処理後のVAD結果リスト
        """

        return_speech_positions: list[SpeechPosition] = []

        for speech_position in speech_positions:

            if len(return_speech_positions) == 0:
                return_speech_positions.append(speech_position)
                continue

            last_speech_position = return_speech_positions[-1]
            if (
                speech_position.start_s - last_speech_position.end_s
                < min_silence_duration_ms_after_vad / 1000
            ):

                last_speech_position.end_s = speech_position.end_s
            else:
                return_speech_positions.append(speech_position)

        return return_speech_positions
