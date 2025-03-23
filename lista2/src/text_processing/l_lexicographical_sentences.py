import sys

def is_lexicographical(sentence):
    words = sentence.split()
    if not words:
        return False

    latest_word = words[0]
    if len(words) > 1:
        for word in words[1:]:
            if word.lower() < latest_word.lower():
                return False
            else:
                latest_word = word
    return True

def lexicographical_sentences(input_stream):
    """
    Prints out sentences from the text stream, of which words are in a lexicographical order.

    :param input_stream: must be in processed format
    """
    for sentence in input_stream:
        if is_lexicographical(sentence):
            sys.stdout.write(sentence)

if __name__ == "__main__":
    lexicographical_sentences(sys.stdin)
