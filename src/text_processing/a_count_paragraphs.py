import sys

def count_paragraphs(input_stream):
    """
    Counts the paragraph in a text stream

    :param input_stream: must be in raw format
    :return: amount of paragraphs in the stream
    """
    paragraphs = 0
    out_of_paragraph = False

    for line in input_stream:
        if not line.strip() and not out_of_paragraph:
            paragraphs += 1
            out_of_paragraph = True
        elif not line.strip():
            continue
        else:
            out_of_paragraph = False

    return paragraphs


if __name__ == "__main__":
    print(count_paragraphs(sys.stdin))
