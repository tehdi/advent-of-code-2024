import logging
import argparse
import re


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
    mul_pattern = re.compile("mul\((\d{1,3}),(\d{1,3})\)")
    multiplicands = []
    for line in input_data:
        logging.debug(line)
        for m in mul_pattern.finditer(line):
            multiplicands.append((int(m.group(1)), int(m.group(2))))
    logging.debug(multiplicands)
    return sum([f[0] * f[1] for f in multiplicands])


def part_two(input_data: list[str], args) -> int:
    dos = [s for s in ''.join(input_data).split('do') if not s.startswith("n't")]
    logging.debug(dos)
    return part_one(dos, args)


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
        logging.info(f"Part 1 (test: 161): {part_one(input_data, args)}")
    elif args.part == 2:
        logging.info(f"Part 2 (test 2: 48): {part_two(input_data, args)}")
