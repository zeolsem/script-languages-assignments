"""Functionality showcase"""
import sys
from text_processing import read_preamble, stream_paragraphs

print(read_preamble(sys.stdin), end='')

for paragraph in stream_paragraphs(sys.stdin, 4096):
    for line in paragraph:
        print(line.rstrip(), end='')
