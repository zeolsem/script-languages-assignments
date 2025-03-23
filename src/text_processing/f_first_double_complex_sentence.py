import sys
from text_processing import stream_phrases


def first_double_complex_sentence(input_stream):
    """
    Finds the first sentence with at least two subordinate clause sub sentences.

    :param input_stream: must be in processed format
    :return: First sentence meeting the condition above in the stream
    """
    for sentence in stream_phrases(input_stream):
        if sentence.count(",") > 1:
            return sentence

    raise ValueError("No sentence meeting the condition found.")


if __name__ == "__main__":
    try:
        sys.stdout.write(first_double_complex_sentence(sys.stdin))
    except ValueError as e:
        print(f"Exception: {e}")