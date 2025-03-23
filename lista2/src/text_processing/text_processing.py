"""
meow
"""
import sys
from typing import TextIO, Generator

from pylint.checkers.utils import returns_bool


def read_preamble(input_stream: TextIO) -> (str | None, bool):
    """
    Reads preamble, if exists, in the streamed document.
    Preamble should be ten lines long at most, and end with
    two empty lines.

    Args:
        input_stream (TextIO): streamed text file

    Returns:
        string: preamble of the text document
    """
    preamble_lines = []
    consecutive_empty_lines = 0
    preamble_found = False

    for _ in range(0, 11):
        current_line = input_stream.readline()
        if not current_line:
            raise ValueError("Text is too short to determine preamble")

        preamble_lines.append(current_line)
        if current_line.strip() == "":
            consecutive_empty_lines += 1
            if consecutive_empty_lines == 2:
                preamble_found = True
                break
        else:
            consecutive_empty_lines = 0

    return preamble_lines, preamble_found
    # if preamble_lines and preamble_found:
    #     return preamble_lines, True
    # return preamble_lines, False


def stream_chunked_text(input_stream: TextIO, chunk_size: int) -> Generator[str, None, None]:
    """
    Streams chunks of specified length from the text stream, until it ends.

    Args:
        input_stream (TextIO): stream to read from
        chunk_size (int): number of characters in each chunk

    Yields:
        str: The chunk of text
    """
    while True:
        chunk = input_stream.read(chunk_size)
        if not chunk:
            break
        yield chunk


def process_line(input_line: str, sentence_buffer: str, eol: bool, raw: bool) -> (list[str], str, bool, bool):
    if '-----' == input_line.strip():
        return [], "", True, True

    if not raw:
        sentence_buffer = sentence_buffer if sentence_buffer == "" else sentence_buffer + " "
    raw_sentences = []

    for char in input_line:
        if raw:
            sentence_buffer += char

        if char in ".!?":
            if not raw:
                sentence_buffer += char
            raw_sentences.append(sentence_buffer)
            sentence_buffer = ""

        elif char == '\n':
            if sentence_buffer and eol == True:
                raw_sentences.append(sentence_buffer)
                sentence_buffer = ""
                break
            eol = True

        else:
            if not raw:
                sentence_buffer += char
            eol = False

    if raw:
        return raw_sentences, sentence_buffer, eol, False

    sentences = []
    for sentence in raw_sentences:
        sentences.append(" ".join(sentence.strip().split('\n')) + '\n')

    return sentences, sentence_buffer, eol, False

def stream_phrases(input_stream: TextIO, skip_preamble: bool = True, raw: bool = False):
    """
    Reads a text stream from an ISBN-compliant text file, generating consecutive sentences.

    Args:
        input_stream (TextIO): stream to read from
        skip_preamble (bool): whether to skip preamble
        raw (bool): whether to do additional formatting - if False, newlines in the middle of sentence
                    are converted to spaces

    Yields:
        str: current sentences of text
    """
    try:
        preamble_candidate, preamble_found = read_preamble(input_stream)
    except ValueError as e:
        sys.stdout.write(f"Exception: {e}")
        return

    if not (skip_preamble and preamble_found):
        for line in preamble_candidate:
            yield line

    end_of_line = False
    sentence_buffer = ""

    for line in input_stream:
        sentences, sentence_buffer, end_of_line, end_of_file = process_line(line, sentence_buffer, end_of_line, raw)
        if end_of_file:
            break
        else:
            for sentence in sentences:
                yield sentence

    if sentence_buffer:
        yield sentence_buffer


if __name__ == "__main__":
    for phrase in stream_phrases(
        sys.stdin,
        skip_preamble="--skip-preamble" in sys.argv,
        raw="--raw" in sys.argv
    ):
        sys.stdout.write(phrase)
