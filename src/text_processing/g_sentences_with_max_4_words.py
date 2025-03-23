import sys


def max_4_words_sentences(input_stream):
    """
    Finds all sentences with at least 4 words.

    :param input_stream: must be in processed format
    """

    for sentence in input_stream:
        if len(sentence.split()) <= 4:
            sys.stdout.write(sentence)


if __name__ == "__main__":
    max_4_words_sentences(sys.stdin)