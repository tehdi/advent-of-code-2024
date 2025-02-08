import logging
import argparse


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
    # for line_index,line in enumerate(input_data):
    for line in input_data:
        # for char_index,char in enumerate(line):
        for char in line:
            pass
    return 0


def part_two(input_data: list[str], args) -> int:
    # for line_index,line in enumerate(input_data):
    for line in input_data:
        # for char_index,char in enumerate(line):
        for char in line:
            pass
    return 0


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
        expected_result = 0
        actual_result = part_one(input_data, args)
        logging.info(f"Part 1: {actual_result} (expected {expected_result}: {actual_result == expected_result})")
    elif args.part == 2:
        expected_result = 0
        actual_result = part_two(input_data, args)
        logging.info(f"Part 2: {actual_result} (expected {expected_result}: {actual_result == expected_result})")
