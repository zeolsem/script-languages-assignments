from typing import Generator
from functools import reduce
import re

from reading_book_content import stream_paragraphs

def readable_characters(generator: Generator[list[str], None, None]):
    acc = 0
    for paragraph in generator:
        for sentence in paragraph:
            acc += reduce(lambda char, amount: (amount + 1 if re.match(r'\S', char) else amount), sentence, 0)