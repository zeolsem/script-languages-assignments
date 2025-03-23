import sys


def longest_sentence(input_stream):
    """
    Counts percentage of sentences with a proper noun in a text stream

    :param input_stream: must be in processed format
    :return: percentage of sentences with a proper noun in the stream
    """
    max_sentence_length = 0
    _longest_sentence = ''
    for line in input_stream:
        if len(line) > max_sentence_length:
            max_sentence_length = len(line)
            _longest_sentence = line
    return _longest_sentence

if __name__ == "__main__":
    print(longest_sentence(sys.stdin))