from enum import Enum

from pydantic import BaseModel

from utils.const.const import Const


class VadResultSpeechType(Enum):

    SPEECH = 1
    NON_SPEECH = 0

    def __str__(self):
        return "SPEECH" if self.value == 1 else "NON_SPEECH"


class VadResult(BaseModel):
    """
    音声区間検出の結果。

    Args:
        start: 開始サンプル数
        end: 終了サンプル数
        type: タイプ（発話区間か無音区間か）
    """

    start: int
    end: int
    sample_rate: int = Const.SAMPLE_RATE
    type: VadResultSpeechType

    def __str__(self):
        return f"VadResult(start={self.start}, end={self.end}, type={self.type})"

    def __repr__(self):
        return f"VadResult(start={self.start}, end={self.end}, type={self.type})"
