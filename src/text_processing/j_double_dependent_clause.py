import sys

def sentences_with_multiple_connectors(input_stream):
    """
    Prints out sentences in a text stream that have at least two connector words

    :param input_stream: must be in processed format
    """
    for sentence in input_stream:
        connector_amount = 0
        for word in sentence.split():
            if word.lower() in ["i", "oraz", "ale", "że", "lub"]:
                connector_amount += 1
            if connector_amount >= 2:
                sys.stdout.write(sentence)
                break

if __name__ == "__main__":
    sentences_with_multiple_connectors(sys.stdin)
