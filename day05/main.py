import logging
import argparse
from collections import defaultdict, deque


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


class Node:
    def __init__(self, value, afters=set(), befores=set()):
        self.value = value
        self.afters = set()
        self.befores = set()

    def copy(self):
        return Node(self.value, set(self.afters), set(self.befores))

    def is_before(self, after: 'Node'):
        self.afters.add(after)
        after.befores.add(self)

    def incoming_count(self):
        return len(self.befores)

    def prune_to(self, node: 'Node'):
        # logging.debug(f'{self.value}: pruning to {node.value if node is not None else "None"}')
        for after in self.afters:
            after.sever_incoming(self)
        self.afters = set()
        if node is not None:
            self.afters.add(node)

    def sever_incoming(self, node: 'Node'):
        self.befores.remove(node)

    def sever_outgoing(self, node: 'Node'):
        self.afters.remove(node)

    def next(self):
        return self.afters[0]

    def __repr__(self):
        return f'Node({self.value}) <- {[b.value for b in self.befores]}'


def part_one(input_data: list[str], args) -> int:
    # test: 97 -> 75 -> 47 -> 61 -> 53 -> 29 -> 13
    # point each node to all of its sub nodes per the page ordering rules
    # find a node that has nothing pointing to it. that's the head
    # find a node that head points to, but nothing else. delete all the other pointers from head
    # continue like that, finding the node that is only pointed to by the current node,
    # then deleting the other outgoing pointers from the current node
    # at the end, you should have a sorted, linked list
    # but actually:
    # hold on to the page ordering rules, but don't do anything with them yet
    # for each update:  get the pages I care about, get the rules involving only those pages, and link together just those rules
    # if an update is valid, find the middle page number and add it to the running total
    mode = 'rules'
    updates = []
    rules = []
    middle_pages_sum = 0

    for line in input_data:
        if line == '':
            mode = 'update'
            continue
        if mode == 'rules':
            rules.append(line)
        elif mode == 'update':
            updates.append([int(page) for page in line.split(',')])

    for update in updates:
        nodes = {}
        applicable_rules = [rule for rule in rules if is_applicable(rule, update)]
        for rule in applicable_rules:
            (before, after) = rule.split('|')
            before = int(before)
            after = int(after)
            if before not in nodes: nodes[before] = Node(before)
            if after not in nodes: nodes[after] = Node(after)
            nodes[before].is_before(nodes[after])

        order = []
        logging.debug(f'count: {len(nodes)}; values: {nodes.values()}')
        head = [node for node in nodes.values() if node.incoming_count() == 0][0]
        current = head
        order.append(head.value)
        while current is not None:
            next_candidates = [node for node in current.afters if node.incoming_count() == 1]
            next = next_candidates[0] if len(next_candidates) == 1 else None
            current.prune_to(next)
            if next is not None: order.append(next.value)
            current = next
        logging.debug(f'order: {order}')

        indexes = []
        for page in update: indexes.append(order.index(page))
        valid = indexes == sorted(indexes)
        logging.debug(f'update: {update}; indexes: {indexes}; valid: {valid}')
        if valid: middle_pages_sum += update[len(update)//2]

    return middle_pages_sum


def is_applicable(rule, update):
    (before, after) = rule.split('|')
    applicable = ((int(before) in update) and (int(after) in update))
    logging.debug(f'checking {rule} against {update}: {applicable}')
    return applicable


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
        expected_result = 143
        actual_result = part_one(input_data, args)
        logging.info(f"Part 1: {actual_result} (expected {expected_result}: {actual_result == expected_result})")
    elif args.part == 2:
        expected_result = 0
        actual_result = part_two(input_data, args)
        logging.info(f"Part 2: {actual_result} (expected {expected_result}: {actual_result == expected_result})")
