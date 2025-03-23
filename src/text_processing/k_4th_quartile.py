import sys


def fourth_quartile_sentences(input_stream):
    """
    Prints out sentences in a text stream that are in the 4th quartile, length-wise

    :param input_stream: must be in processed format and must contain preamble
    """
    sentences = list(input_stream)
    if not sentences:
        return

    lengths = sorted(len(s) for s in sentences)
    threshold = lengths[int(0.75 * len(lengths))]  

    for sentence in sentences:
        if len(sentence) >= threshold:
            sys.stdout.write(" ".join(sentence.split('\n')) + '\n')

if __name__ == "__main__":
    fourth_quartile_sentences(sys.stdin)
