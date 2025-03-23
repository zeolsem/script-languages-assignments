import sys
import re


def nonwhite_characters(input_stream):
    """
    Counts non-white characters in a text stream

    :param input_stream: can be in either raw or processed format
    :return: amount of non-white characters in the stream
    """
    chars = 0
    for line in input_stream:
        for char in line:
            if re.match(r'[\S]', char):
                chars += 1

    return chars


if __name__ == "__main__":
    print(nonwhite_characters(sys.stdin))