import sys


def questions_or_exclamations(input_stream):
    """
    Prints out sentences in a text stream that are exclamations or questions.

    :param input_stream: must be in processed format
    """
    for sentence in input_stream:
        if sentence.strip().endswith(("?", "!")):
            sys.stdout.write(sentence)


if __name__ == "__main__":
    questions_or_exclamations(sys.stdin)
