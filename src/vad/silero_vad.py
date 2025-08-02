from pathlib import Path

import soundfile as sf
from pydantic import BaseModel
from silero_vad import get_speech_timestamps, load_silero_vad, read_audio

from model.value_object.speech_position import SpeechPosition


class SileroVadConfig(BaseModel):
    """
    StereoVadの設定

    Args:
        threshold: 発話判定の閾値。この値以上の確率で発話と判定
        min_speech_duration_ms: 最小発話時間（ミリ秒）。これより短い発話は除外
        max_speech_duration_s: 最大発話時間（秒）。これより長い場合は分割
        min_silence_duration_ms: 発話区間を分離するための最小無音時間
        speech_pad_ms: 発話区間の前後に追加する無声音区間の長さ（ミリ秒）
        neg_threshold: 無音判定の閾値（発話状態から無音状態への遷移用）
    """

    threshold: float = 0.25
    min_speech_duration_ms: int = 200
    max_speech_duration_s: float = float("inf")
    min_silence_duration_ms: int = 500
    speech_pad_ms: int = 250
    neg_threshold: float = 0.25
    min_silence_duration_ms_after_vad: int = 0


class SileroVad:
    def __init__(self, config: SileroVadConfig = SileroVadConfig()):
        self.config = config
        self.model = load_silero_vad(onnx=True)

    def execute_vad(self, wav_path: Path) -> list[SpeechPosition]:
        """
        Args:
            wav_path: 音声ファイルのパス

        Returns:
            list[VadResult]: 音声区間のリスト
        """

        _, sample_rate = sf.read(wav_path)

        speech_positions = self._execute_silero_vad(wav_path, sample_rate)

        concatinated_speech_positions = self._concatinate_speech_vad_results(
            speech_positions,
            min_silence_duration_ms_after_vad=self.config.min_silence_duration_ms_after_vad,
        )

        return concatinated_speech_positions

    def _execute_silero_vad(
        self, wav_path: Path, sample_rate: int
    ) -> list[SpeechPosition]:
        """
        Args:
            wav_path: 音声ファイルのパス

        Returns:
            list[VadResult]: 音声区間のリスト(発話区間のみ)
        """

        wav = read_audio(str(wav_path), sample_rate)
        speech_timestamps = get_speech_timestamps(
            wav,
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
            return_results.append(
                SpeechPosition(
                    start_s=timestamp["start"] / sample_rate,
                    end_s=timestamp["end"] / sample_rate,
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
            list[VadResult]: 結合処理後のVAD結果リスト
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
