from model.value_object.speech_position import SpeechPosition


def convert_ATR503_format_from(one_based_index: int) -> str:
    """
    1-indexをATR503の形式に変換する

    変換は以下のように行う
    1 -> A01
    50 -> A50
    51 -> B01
    100 -> B50
    ...
    500 -> J50

    (特殊)
    501 -> J51
    502 -> J52
    503 -> J53

    Args:
        one_based_index: 1-index

    Returns:
        ATR503の形式
    """

    if one_based_index < 1:
        raise ValueError("indexは1以上である必要があります")

    alphabet = ""
    if one_based_index < 500:
        alphabet = chr((one_based_index - 1) // 50 + ord("A"))
    else:
        alphabet = "J"

    number = str((one_based_index - 1) % 50 + 1).zfill(2)
    if one_based_index > 500:
        number = str(int(number) + 50)

    return alphabet + number


def convert_index_from_ATR503_format(atr503_format: str) -> int:

    if atr503_format == "J51":
        return 501
    elif atr503_format == "J52":
        return 502
    elif atr503_format == "J53":
        return 503

    alphabet = atr503_format[0]
    number = atr503_format[1:]
    return int(number) + (ord(alphabet) - ord("A")) * 50
