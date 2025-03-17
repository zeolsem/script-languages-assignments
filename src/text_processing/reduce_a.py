from typing import Generator
from functools import reduce

def count_paragraphs(generator: Generator[list[str], None, None]) -> int:
    # acc = 0
    # for lst in generator:
    #     acc += 1
    # return acc
    return reduce(lambda acc, _: acc + 1, generator, 0)

