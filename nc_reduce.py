#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby


def uniq_count(items, min_count=2):
    for item, entries in groupby(items):
        count = sum(1 for _ in entries)
        if count > min_count:
            yield item, count


if __name__ == '__main__':
    import fileinput
    iterable = map(str.strip, fileinput.input())
    for items in uniq_count(iterable):
        print(*items, sep='\t')

# similar to:
# LC_ALL=C uniq -c | LC_ALL=C awk '{ if ($1 > 2) print $0 }'
# use awk to output the same format
# LC_ALL=C uniq -c | LC_ALL=C awk '{c=$1; $1=""; if (c > 2) print $0 "\t" c }'
