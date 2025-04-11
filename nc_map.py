#!/usr/bin/env python
# -*- coding: utf-8 -*-


def ngrams(tokens, n):
    for ngram in zip(*(tokens[i:] for i in range(n))):
        yield ngram


def gen_all_ngrams(tokens, max_len=5):
    for n in range(1, max_len+1):
        for ngram in ngrams(tokens, n):
            yield ngram


def ngramcount_map(lines):
    for line in lines:
        for ngram in gen_all_ngrams(line.split()):
            yield ngram


if __name__ == '__main__':
    import fileinput
    for ngram in ngramcount_map(fileinput.input()):
        print(*ngram)
