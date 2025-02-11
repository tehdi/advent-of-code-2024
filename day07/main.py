import logging
import argparse
import itertools


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


def plus(a, b): return a + b

def multiply(a, b): return a * b

def concatenate(a, b): return int(str(a) + str(b))


class EquationV1:
    def __init__(self, test_value, numbers):
        self.test_value = test_value
        self.numbers = numbers

    def try_solve(self):
        operators_needed = len(self.numbers) - 1
        max_trials = 2**operators_needed
        for i in range(max_trials):
            operators = [
                plus if o == '0' else multiply
                for o in "{0:b}".format(i).zfill(operators_needed)
            ]
            operators.insert(0, plus)
            steps = itertools.zip_longest(operators, self.numbers)
            # logging.debug([s for s in steps])
            total = 0
            for step in steps:
                total = step[0](total, step[1])
            logging.debug(f"{self.test_value}: {total}?")
            if total == self.test_value: return total
        return 0

    def __repr__(self):
        return f"{self.test_value} = {self.numbers}"


# https://stackoverflow.com/a/28666223
def number_to_base(number, base):
    if number == 0: return '0'
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return ''.join([str(d) for d in digits[::-1]])


def pick_function(operator):
    logging.debug(f"finding operator function for {operator}")
    if operator == '0': return plus
    if operator == '1': return multiply
    if operator == '2': return concatenate
    return None


class EquationV2:
    def __init__(self, test_value, numbers):
        self.test_value = test_value
        self.numbers = numbers

    def try_solve(self):
        operator_options = 3
        operators_needed = len(self.numbers) - 1
        max_trials = operator_options**operators_needed
        for i in range(max_trials):
            operators = [
                pick_function(o)
                for o in number_to_base(i, operator_options).zfill(operators_needed)
            ]
            operators.insert(0, plus)
            total = 0
            steps = itertools.zip_longest(operators, self.numbers)
            for step in steps: total = step[0](total, step[1])
            logging.debug(f"{self.test_value}: {total}?")
            if total == self.test_value: return total
        return 0

    def __repr__(self):
        return f"{self.test_value} = {self.numbers}"


def part_one(input_data: list[str], args) -> int:
    equations = []
    for line in input_data:
        test_value = int(line.split(':')[0])
        numbers = [int(n) for n in line.split(': ')[1].split(' ')]
        equations.append(EquationV1(test_value, numbers))
    total_calibration_result = sum(e.try_solve() for e in equations)
    return total_calibration_result


# Yes, it takes a while to run. No, I don't think it would reasonably extend to 4 operator options.
def part_two(input_data: list[str], args) -> int:
    equations = []
    for line in input_data:
        test_value = int(line.split(':')[0])
        numbers = [int(n) for n in line.split(': ')[1].split(' ')]
        equations.append(EquationV2(test_value, numbers))
    total_calibration_result = sum(e.try_solve() for e in equations)
    return total_calibration_result


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
        expected_result = 3749
        actual_result = part_one(input_data, args)
        logging.info(f"Part 1: {actual_result} (test: {expected_result} = {actual_result == expected_result})")
    elif args.part == 2:
        expected_result = 11387
        actual_result = part_two(input_data, args)
        logging.info(f"Part 2: {actual_result} (test: {expected_result} = {actual_result == expected_result})")
