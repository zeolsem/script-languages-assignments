import sys


def percentage_of_sentences_with_proper_nouns(input_stream):
    """
    Counts percentage of sentences with a proper noun in a text stream

    :param input_stream: must be in processed format
    :return: percentage of sentences with a proper noun in the stream
    """
    total_sentences = 0
    proper_noun_sentences = 0

    for sentence in input_stream:
        total_sentences += 1
        for word in sentence.split()[1:]:
            if word[0].isupper():
                proper_noun_sentences += 1
                break

    percentage = (proper_noun_sentences / total_sentences) * 100 if total_sentences > 0 else 0
    return f"{percentage:.2f}%"


if __name__ == "__main__":
    print(percentage_of_sentences_with_proper_nouns(sys.stdin))