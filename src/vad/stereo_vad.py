from pathlib import Path

import soundfile as sf
from pydantic import BaseModel
from silero_vad import get_speech_timestamps, load_silero_vad, read_audio

from model.value_object.vad_result import VadResult, VadResultSpeechType
from utils.const.const import Const


class StereoVadConfig(BaseModel):
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
    min_silence_duration_ms: int = 800
    speech_pad_ms: int = 250
    neg_threshold: float = 0.25


class StereoVad:
    def __init__(self, config: StereoVadConfig = StereoVadConfig()):
        self.config = config
        self.model = load_silero_vad(onnx=True)

    def execute_vad(self, wav_path: Path) -> list[VadResult]:
        """
        Args:
            wav_path: 音声ファイルのパス

        Returns:
            list[VadResult]: 音声区間のリスト
        """

        _, sample_rate = sf.read(wav_path)
        speech_vad_results, total_samples = self._get_speech_vad_result(
            wav_path, sample_rate
        )

        concatinated_vad_results = self._concatinate_vad_results(
            speech_vad_results, min_silence_duration_ms=0
        )

        speech_vad_results_with_non_speech = (
            self._get_speech_vad_result_with_non_speech(
                concatinated_vad_results, total_samples
            )
        )

        return speech_vad_results_with_non_speech

    def _get_speech_vad_result(
        self, wav_path: Path, sample_rate: int
    ) -> tuple[list[VadResult], int]:
        """
        Args:
            wav_path: 音声ファイルのパス

        Returns:
            list[VadResult]: 音声区間のリスト
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

        return_results: list[VadResult] = []

        for timestamp in speech_timestamps:
            return_results.append(
                VadResult(
                    start=timestamp["start"],
                    end=timestamp["end"],
                    type=VadResultSpeechType.SPEECH,
                )
            )

        return return_results, wav.shape[0]

    def _get_speech_vad_result_with_non_speech(
        self, speech_vad_results: list[VadResult], total_samples: int
    ) -> list[VadResult]:
        """
        Args:
            speech_vad_results: 音声区間のリスト
            total_samples: 音声データの総サンプル数

        Returns:
            list[VadResult]: 音声区間のリスト
        """
        return_results: list[VadResult] = []

        # speech_timestampsが空の場合、全体を無声音として扱う
        if not speech_vad_results:
            return_results.append(
                VadResult(
                    start=0,
                    end=total_samples,
                    type=VadResultSpeechType.NON_SPEECH,
                )
            )
            return return_results

        current_sample = 0

        for speech_vad_result in speech_vad_results:
            start_sample = speech_vad_result.start
            end_sample = speech_vad_result.end

            # 前の区間の終了から現在の有声音区間の開始までの無声音区間を追加
            if current_sample < start_sample:
                return_results.append(
                    VadResult(
                        start=current_sample,
                        end=start_sample,
                        type=VadResultSpeechType.NON_SPEECH,
                    )
                )

            # 有声音区間を追加
            return_results.append(
                VadResult(
                    start=start_sample,
                    end=end_sample,
                    type=VadResultSpeechType.SPEECH,
                )
            )

            current_sample = end_sample

        # 最後の有声音区間の後に残りの無声音区間があれば追加
        if current_sample < total_samples:
            return_results.append(
                VadResult(
                    start=current_sample,
                    end=total_samples,
                    type=VadResultSpeechType.NON_SPEECH,
                )
            )

        return return_results

    def _concatinate_vad_results(
        self,
        speech_vad_results: list[VadResult],
        min_silence_duration_ms: int = 1000,
        sample_rate: int = Const.SAMPLE_RATE,
    ) -> list[VadResult]:
        """
        Args:
            vad_results: VAD結果のリスト

        Returns:
            list[VadResult]: 結合処理後のVAD結果リスト
        """

        return_results: list[VadResult] = []

        for speech_vad_result in speech_vad_results:

            if len(return_results) == 0:
                return_results.append(speech_vad_result)
                continue

            last_result = return_results[-1]
            if (
                speech_vad_result.start - last_result.end
                < min_silence_duration_ms * sample_rate / 1000
            ):

                last_result.end = speech_vad_result.end
            else:
                return_results.append(speech_vad_result)

        return return_results
