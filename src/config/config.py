from pathlib import Path

import yaml
from pydantic import BaseModel


class SileroVadConfig(BaseModel, frozen=True):
    """
    StereoVadの設定

    Args:
        threshold: 発話判定の閾値。この値以上の確率で発話と判定
        min_speech_duration_ms: 最小発話時間（ミリ秒）。これより短い発話は除外
        max_speech_duration_s: 最大発話時間（秒）。これより長い場合は分割
        min_silence_duration_ms: 発話区間を分離するための最小無音時間
        speech_pad_ms: 発話区間の前後に追加する無声音区間の長さ（ミリ秒）
        neg_threshold: 無音判定の閾値（発話状態から無音状態への遷移用）
        min_silence_duration_ms_after_vad: 発話区間を分離するための最小無音時間（ミリ秒）
    """

    threshold: float = 0.25
    min_speech_duration_ms: int = 200
    max_speech_duration_s: float = float("inf")
    min_silence_duration_ms: int = 250
    speech_pad_ms: int = 250
    neg_threshold: float = 0.25
    min_silence_duration_ms_after_vad: int = 500

    @classmethod
    def load_from_yaml(cls, yaml_path: Path) -> "SileroVadConfig":
        if not yaml_path.exists():
            return cls()

        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f) or {}

        return cls(**data)
