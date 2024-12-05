import logging
import argparse
from collections import Counter


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
    safe_reports = 0
    for line in input_data:
        levels = [int(i) for i in line.split()]
        # duplicates aren't allowed
        if len(set(levels)) != len(levels):
            logging.debug(f'{levels} has duplicates')
            continue
        # levels must be in strictly increasing or decreasing order
        if sorted(levels) != levels and sorted(levels, reverse=True) != levels:
            logging.debug(f"{levels} isn't increasing or decreasing")
            continue
        max_diff = max([abs(levels[i] - levels[i+1]) for i in range(len(levels) - 1)])
        if max_diff > 3:
            logging.debug(f"{levels} has a too-large diff ({max_diff})")
            continue
        logging.debug(f"{levels} is safe")
        safe_reports += 1
    return safe_reports


class Report:
    report_id = 0

    def id_gen():
        Report.report_id += 1
        yield Report.report_id

    def __init__(self, levels):
        self.id = next(Report.id_gen())
        self.original_levels = levels
        self.versions = [levels] + [
            [levels[i] for i in range(len(levels)) if i != skip_index]
            for skip_index in range(len(levels))
        ]

    def has_more_versions(self):
        logging.debug(f"{self}")
        return len(self.versions) > 0

    def remove_duplicates(self):
        logging.debug(f"duplicate-checking {self.id}")
        self.versions = [levels for levels in self.versions if len(levels) == len(set(levels))]

    def remove_unordered(self):
        logging.debug(f"order-checking {self.id}")
        self.versions = [
            levels for levels in self.versions
            if levels == sorted(levels) or levels == sorted(levels, reverse=True)
        ]

    def remove_gaps(self):
        logging.debug(f"gap-checking {self.id}")
        self.versions = [
            levels for levels in self.versions
            if max([abs(levels[i+1] - levels[i]) for i in range(len(levels) - 1)]) <= 3
        ]

    def remove_excess_removals(self):
        logging.debug(f"removal-checking {self.id}")
        self.versions = [levels for levels in self.versions if len(levels) >= len(self.original_levels) - 1]

    def validators(self):
        yield self.remove_duplicates
        yield self.remove_unordered
        yield self.remove_gaps
        yield self.remove_excess_removals

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.id}: {self.original_levels} => {self.versions}"


def part_two(input_data: list[str], args) -> int:
    safe_reports = []
    reports = []
    for line in input_data:
        levels = [int(i) for i in line.split()]
        report = Report(levels)
        reports.append(report)

    for report in reports:
        for validator in report.validators(): validator()
        if report.has_more_versions(): safe_reports.append(report)

    logging.debug(f"Made the cut:")
    logging.debug('\n'.join(str(report) for report in safe_reports))

    return len(safe_reports)


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
        logging.info(f"Part 1 (test: 2): {part_one(input_data, args)}")
    elif args.part == 2:
        logging.info(f"Part 2 (test: 6): {part_two(input_data, args)}")
