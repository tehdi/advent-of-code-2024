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


EMPTY = '.'
OBSTACLE = '#'
GUARD = '^'
VISITED = 'X'

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'
STEP_INDEX = 0
ROW_INDEX = 0
COLUMN_INDEX = 1
NEW_FACING_INDEX = 1
# current facing = ((row delta, column delta), turn to face)
movement = {
    UP: ((-1, 0), RIGHT),
    DOWN: ((+1, 0), LEFT),
    LEFT: ((0, -1), UP),
    RIGHT: ((0, +1), DOWN),
}


def print_map(guard_position, facing, obstacles, visited, max_row, max_column):
    logging.debug(f"{guard_position} {facing} {visited}")
    for row_index in range(max_row + 1):
        row = ''
        for column_index in range(max_column + 1):
            if (row_index, column_index) == guard_position: row += facing
            elif (row_index, column_index) in obstacles: row += OBSTACLE
            elif (row_index, column_index) in visited: row += VISITED
            elif ((row_index, column_index), facing) in visited: row += VISITED
            else: row += EMPTY
        logging.debug(row)


def in_range(position, max_row, max_column):
    row = position[ROW_INDEX]
    column = position[COLUMN_INDEX]
    return row >= 0 and row <= max_row and column >= 0 and column <= max_row


# How many distinct positions will the guard visit before leaving the mapped area?
def part_one(input_data: list[str], args) -> int:
    obstacles = set()
    max_row = len(input_data) - 1
    for row_index,row in enumerate(input_data):
        max_column = len(row) - 1
        for col_index,char in enumerate(row):
            position = (row_index, col_index)
            if char == GUARD:
                guard_position = position
            elif char == OBSTACLE:
                obstacles.add(position)
    facing = UP
    visited = set()
    visited.add(guard_position)
    logging.debug(obstacles)
    logging.debug(max_row)
    logging.debug(max_column)
    logging.debug(visited)
    while True:
        movement_delta = movement[facing][STEP_INDEX]
        new_position = (guard_position[ROW_INDEX] + movement_delta[ROW_INDEX], guard_position[COLUMN_INDEX] + movement_delta[COLUMN_INDEX])
        if not in_range(new_position, max_row, max_column):
            logging.debug(f"{new_position} is outside of lab: {len(visited)}")
            break
        if new_position in obstacles:
            facing = movement[facing][NEW_FACING_INDEX]
            logging.debug(f"{new_position} is an obstacle. turning to {facing}: {len(visited)}")
        else:
            visited.add(new_position)
            logging.debug(f"moving to {new_position}: {len(visited)}")
            guard_position = new_position
        print_map(guard_position, facing, obstacles, visited, max_row, max_column)
    return len(visited)


# How many different spots can I place an obstacle to put the guard into a loop?
def part_two(input_data: list[str], args) -> int:
    obstacles = set()
    new_obstacle_options = set()
    max_row = len(input_data) - 1
    for row_index,row in enumerate(input_data):
        max_column = len(row) - 1
        for col_index,char in enumerate(row):
            position = (row_index, col_index)
            if char == GUARD:
                initial_guard_position = position
            elif char == OBSTACLE:
                obstacles.add(position)
            else: new_obstacle_options.add(position)
    new_obstacle_loops = set()
    for new_obstacle_position in new_obstacle_options:
        logging.debug(f"trying new obstacle at {new_obstacle_position}")
        guard_position = initial_guard_position
        facing = UP
        visited = set()
        visited.add((guard_position, facing))
        while True:
            movement_delta = movement[facing][STEP_INDEX]
            new_position = (guard_position[ROW_INDEX] + movement_delta[ROW_INDEX], guard_position[COLUMN_INDEX] + movement_delta[COLUMN_INDEX])
            if not in_range(new_position, max_row, max_column):
                logging.debug(f"{new_position} is outside of lab")
                break
            if new_position in obstacles or new_position == new_obstacle_position:
                facing = movement[facing][NEW_FACING_INDEX]
                logging.debug(f"{new_position} is an obstacle. turning to {facing}")
                # print_map(guard_position, facing, obstacles, visited, max_row, max_column)
                if (guard_position, facing) in visited:
                    logging.info(f"found ({guard_position}, {facing}) in visited; {new_obstacle_position} creates a loop")
                    new_obstacle_loops.add(new_obstacle_position)
                    break
                else: visited.add((guard_position, facing))
            else:
                visited.add((new_position, facing))
                logging.debug(f"moving to {new_position}")
                guard_position = new_position
            # print_map(guard_position, facing, obstacles, visited, max_row, max_column)
    return len(new_obstacle_loops)


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
        expected_result = 41
        actual_result = part_one(input_data, args)
        logging.info(f"Part 1: {actual_result} (test: {expected_result} = {actual_result == expected_result})")
    elif args.part == 2:
        expected_result = 6
        actual_result = part_two(input_data, args)
        logging.info(f"Part 2: {actual_result} (test: {expected_result} = {actual_result == expected_result})")
