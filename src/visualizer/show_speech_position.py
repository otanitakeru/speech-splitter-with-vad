from model.value_object.speech_position import SpeechPosition


def show_speech_position(speech_positions: list[SpeechPosition]):
    """
    音声位置情報を見やすい形式で表示する

    Args:
        speech_positions: 音声位置のリスト
    """
    if not speech_positions:
        print("🔇 音声セグメントが見つかりませんでした")
        return

    print("\n")
    print(f"🎤 音声セグメント情報 (合計: {len(speech_positions)}個)")
    print("=" * 60)

    total_duration = 0

    for i, speech_position in enumerate(speech_positions, 1):
        duration = speech_position.end_s - speech_position.start_s
        total_duration += duration

        print(
            f"{i:3d}: "
            f"{speech_position.start_s:7.2f}s - {speech_position.end_s:7.2f}s "
            f"(長さ: {duration:6.2f}s)"
        )

    print("=" * 60)
    print("\n")
