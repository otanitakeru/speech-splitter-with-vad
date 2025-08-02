from ATR503.formatter import (
    convert_ATR503_format_from,
    convert_index_from_ATR503_format,
)


def test():
    for i in range(1, 504):
        if convert_ATR503_format_from(i) != convert_ATR503_format_from(
            convert_index_from_ATR503_format(convert_ATR503_format_from(i))
        ):
            print(f"{i}: {convert_ATR503_format_from(i)}")
            print(f"{convert_index_from_ATR503_format(convert_ATR503_format_from(i))}")
            raise ValueError("test failed")


if __name__ == "__main__":
    test()
