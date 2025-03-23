from typing import TextIO

from text_processing import read_preamble
from text_processing import stream_chunked_text


def read_at(text_stream: TextIO, pos: int):
    _curr = text_stream.tell()
    text_stream.seek(pos)
    character = text_stream.read(1)
    text_stream.seek(_curr)
    return character


def peek_line(text_stream: TextIO) -> str:
    """Helps peek the line in the stream"""
    pos = text_stream.tell()
    _line = text_stream.readline()
    text_stream.seek(pos)
    return _line


def stream_paragraphs(input_stream: TextIO, chunk_size: int = 4096, skip_preamble: bool = True):
    """
    Generator function that yields consecutive paragraphs from the text stream provided

    Args:
        input_stream (TextIO): stream to process
        chunk_size (int): how many characters should be in a chunk of the stream.
        skip_preamble (bool): set to true if the preamble needs to be skipped

    Yields:
        list[str]: list of individual sentences in the paragraph.
    """
    if not skip_preamble:
        read_preamble(input_stream)

    _paragraph: list[str] = []
    pos = input_stream.tell()
    buffer = ''
    eol = False # end of line
    consecutive_divisors = 0
    failed_tries = 0

    for chunk in stream_chunked_text(input_stream, chunk_size):
        if not chunk:
            break

        # handling incoming characters
        for char in chunk:
            buffer += char
            if char == '\n' and eol:
                # new paragraph
                eol = False
                failed_tries = 0
                if len(_paragraph) != 0:
                    yield _paragraph
                pos = input_stream.tell()
                _paragraph.clear()
            elif char in '.!?':
                # new sentence
                _paragraph.append(buffer)
                buffer = ''
            elif char == '\n':
                eol = True

            # handle publisher information
            consecutive_divisors = consecutive_divisors + 1 if char == '-' else 0
            if consecutive_divisors == 5 and len(buffer) < 128 and buffer.strip().split('\n').pop() == '-----':
                _paragraph.append(buffer.rstrip()[:-5])
                yield _paragraph
                return


        # if there is a paragraph that extends beyond this chunk, increase fail counter
        if len(_paragraph) != 0:
            input_stream.seek(pos)
            failed_tries += 1
        # if the paragraph is bigger than a chunk, make future chunks bigger
        if failed_tries >= 2:
            chunk_size *= 2

    # if there is an unifinished line - the file does not end with CR or \n - add it to the paragraph
    if len(buffer) != 0:
        _paragraph.append(buffer)
    if len(_paragraph) != 0:
        yield _paragraph
        _paragraph.clear()
