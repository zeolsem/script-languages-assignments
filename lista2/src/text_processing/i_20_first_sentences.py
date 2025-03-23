import sys
from typing import TextIO


def first_20_sentences(input_stream: TextIO):
    """
    Prints out first 20 sentences in a text stream

    :param input_stream: must be in processed format
    """
    count = 0
    for sentence in input_stream:
        sys.stdout.write(sentence)
        count += 1
        if count >= 20:
            break


if __name__ == "__main__":
    first_20_sentences(sys.stdin)
