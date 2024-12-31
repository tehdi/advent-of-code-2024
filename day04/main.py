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


LETTER_X = "X"
LETTER_M = "M"
LETTER_A = "A"
LETTER_S = "S"


N = "N"
NE = "NE"
E = "E"
SE = "SE"
S = "S"
SW = "SW"
W = "W"
NW = "NW"
UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1
HORIZONTAL = 0
VERTICAL = 1

class Coord:
    def __init__(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical

    def to_the(self, direction):
        return Coord(
            self.horizontal + DIRECTION[direction][HORIZONTAL],
            self.vertical + DIRECTION[direction][VERTICAL]
        )

    def __repr__(self):
        return f"({self.horizontal}, {self.vertical})"


DIRECTION = {
    N: (0, UP),    NE: (RIGHT, UP),
    E: (RIGHT, 0), SE: (RIGHT, DOWN),
    S: (0, DOWN),  SW: (LEFT, DOWN),
    W: (LEFT, 0),  NW: (RIGHT, UP)
}


class XmasFinder:
    def __init__(self, h, v):
        self.definitely_x = Coord(h, v)
        self.xmas_directions = set()

    def is_xmas(self, direction, grid):
        maybe_m = self.definitely_x.to_the(direction)
        maybe_a = maybe_m.to_the(direction)
        maybe_s = maybe_a.to_the(direction)

        min_horizontal = 0
        max_horizontal = len(grid[0]) - 1
        min_vertical = 0
        max_vertical = len(grid) - 1
        horizontals = [d.horizontal for d in [maybe_m, maybe_a, maybe_s]]
        verticals = [d.vertical for d in [maybe_m, maybe_a, maybe_s]]
        if (min(horizontals) < min_horizontal or max(horizontals) > max_horizontal or
                min(verticals) < min_vertical or max(verticals) > max_vertical):
            return False

        is_xmas = (grid[maybe_m.vertical][maybe_m.horizontal] == LETTER_M and
            grid[maybe_a.vertical][maybe_a.horizontal] == LETTER_A and
            grid[maybe_s.vertical][maybe_s.horizontal] == LETTER_S)
        if is_xmas: self.xmas_directions.add(direction)
        return is_xmas

    def count(self):
        return len(self.xmas_directions)

    def __repr__(self):
        return f"{self.definitely_x}: {self.xmas_directions} ({self.count()})"


def part_one(input_data: list[str], args) -> int:
    xmas_finders = []
    for line_index,line in enumerate(input_data):
        for char_index,char in enumerate(line):
            if char == LETTER_X: xmas_finders.append(XmasFinder(char_index, line_index))
    for xmas_finder in xmas_finders:
        for direction in DIRECTION.keys():
            xmas_finder.is_xmas(direction, input_data)
        logging.debug(xmas_finder)
    return sum([xmas_finder.count() for xmas_finder in xmas_finders])


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
        logging.info(f"Part 1 (test: 18): {part_one(input_data, args)}")
    elif args.part == 2:
        logging.info(f"Part 2 (test: 0): {part_two(input_data, args)}")
