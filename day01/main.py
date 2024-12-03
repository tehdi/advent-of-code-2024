import logging
import argparse
from collections import defaultdict


def configure_logging(verbose, output_file):
    log_level = logging.DEBUG if verbose else logging.INFO
    if output_file is None:
        logging.basicConfig(
            format='%(message)s',
            level=log_level
        )
    else:
        logging.basicConfig(
            format='%(message)s',
            level=log_level,
            filename=output_file,
            filemode='w'
        )


def part_one(input_data: list[str], args) -> int:
    left = []
    right = []
    for line in input_data:
        (l, r) = line.split()
        left.append(int(l))
        right.append(int(r))
    merged = zip(sorted(left), sorted(right))
    diffs = [abs(one - two) for one, two in merged]
    logging.debug(diffs)
    return sum(diffs)


def part_two(input_data: list[str], args) -> int:
    left = defaultdict(int)
    right = defaultdict(int)
    for line in input_data:
        (l, r) = line.split()
        left[int(l)] += 1
        right[int(r)] += 1
    sim_score = sum([lk * right[lk] * lv for lk, lv in left.items()])
    return sim_score


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', default=None)
    parser.add_argument('-o', '--output-file', default=None)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('-p', '--part', type=int, default=1)
    args = parser.parse_args()
    configure_logging(args.verbose, args.output_file)

    filename = args.input_file
    with open(filename) as input_file:
        input_data = [line.rstrip('\n') for line in input_file]
    if args.part == 1:
        logging.info(f"Part 1 (test: 0): {part_one(input_data, args)}")
    elif args.part == 2:
        logging.info(f"Part 2 (test: 0): {part_two(input_data, args)}")
