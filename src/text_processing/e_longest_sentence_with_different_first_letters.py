import sys


def longest_unique_adjacent_sentence(input_stream):
    """
    Finds the longest sentence with different first letters in each word in a text stream

    :param input_stream: must be in processed format
    :return: Longest sentence meeting the condition above in the stream
    """
    longest_valid_sentence = ""

    for sentence in input_stream:
        used_letters = ""
        is_valid = True
        for word in sentence.split():
            if word[0].lower() in used_letters:
                is_valid = False
                break
            else:
                used_letters += word[0].lower()

        if is_valid:
            if len(sentence) > len(longest_valid_sentence):
                longest_valid_sentence = sentence

    return longest_valid_sentence

if __name__ == "__main__":
    sys.stdout.write(longest_unique_adjacent_sentence(sys.stdin))
