"""
meow
"""
from typing import TextIO, Generator

from pylint.checkers.utils import is_comprehension


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


def read_preamble(input_stream: TextIO) -> str | None:
    """
    Reads preamble, if exists, in the streamed document.
    Preamble should be ten lines long at most, and end with
    two empty lines.

    Args:
        input_stream (TextIO): streamed text file

    Returns:
        string: preamble of the text document
    """
    preamble = ''
    for _ in range(0, 11):
        current_line = input_stream.readline()
        if len(current_line.rstrip()) == len(peek_line(input_stream).rstrip()) == 0:
            input_stream.readline()
            return preamble
        preamble += current_line

    input_stream.seek(0)
    return None


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

def process_chunk(chunk: str, divisors: int,
                  eol: bool) -> tuple[list[str], int, bool, bool]:
    _paragraph: list[str] = []
    buffer: str = ''

    for char in chunk:
        buffer += char
        if char == '\n' and eol:
            # new paragraph
            eol = False
            if len(_paragraph) != 0:
                return _paragraph, divisors, eol, True
            _paragraph.clear()
        elif char in '.!?':
            # new sentence
            _paragraph.append(buffer)
            buffer = ''
        elif char == '\n':
            eol = True

        divisors += 1 if char == '=' else 0
        if divisors == 5 and buffer.strip().split('\n').pop() == '-----':
            divisors = 0
            _paragraph.append(buffer.rstrip()[:-5])
            return _paragraph, divisors, eol, True

        return [], 0, False, False


def stream_paragraphs(input_stream: TextIO, chunk_size: int, skip_preamble: bool = True) -> Generator[list[str], None, None]:
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
    buffer = ''
    eol = False # end of line
    consecutive_divisors = 0
    failed_tries = 0
    is_complete = True

    for chunk in stream_chunked_text(input_stream, chunk_size):
        if not chunk:
            break

        # handling incoming characters
        # for char in chunk:
        #     buffer += char
        #     if char == '\n' and eol:
        #         # new paragraph
        #         eol = False
        #         failed_tries = 0
        #         if len(_paragraph) != 0:
        #             yield _paragraph
        #         pos = input_stream.tell()
        #         _paragraph.clear()
        #     elif char in '.!?':
        #         # new sentence
        #         _paragraph.append(buffer)
        #         buffer = ''
        #     elif char == '\n':
        #         eol = True
        #
        #     # handle publisher information
        #     consecutive_divisors += 1 if char == '-' else 0
        #     if consecutive_divisors == 5 and buffer.strip().split('\n').pop() == '-----':
        #         _paragraph.append(buffer.rstrip()[:-5])
        #         yield _paragraph
        #         return
        #
        pos = input_stream.tell()
        _paragraph, consecutive_divisors, eol, is_complete = process_chunk(input_stream, chunk, consecutive_divisors, eol)

        # if there is a paragraph that extends beyond this chunk, increase fail counter
        if not is_complete:
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

