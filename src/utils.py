from . import Path, itertools


def pattern_match(pattern, sequence):
    """Count the number of times that pattern occurs in the sequence."""
    pattern = tuple(pattern)
    k = len(pattern)

    # create k iterators for the sequence
    i = itertools.tee(sequence, k)

    # advance the iterators
    for j in range(k):
        for _ in range(j):
            next(i[j])

    count = 0
    for q in zip(*i):
        if pattern == q:
            count += 1

    return count


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()