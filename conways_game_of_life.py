from collections import defaultdict

# constraints for conways game of life coords
MIN_64BIT_INT = -2**63
MAX_64BIT_INT = 2**63 - 1

def parse_life_106_string(life_106_string: str) -> set:
    """
    :param life_106_string: string in Life 1.06 format
    :return: a set of tuples representing live cells in a conway's game of life simulation
    """
    lines = life_106_string.strip().splitlines()
    if not lines or lines[0] != "#Life 1.06":
        raise ValueError("Invalid Life 1.06 format: Missing or incorrect header.")

    # using set to represent live cells to handle the possibility of same cell listed twice
    live_cells = set()
    # skip initial #Life 1.06 line
    for line in lines[1:]:
        try:
            x, y = map(int, line.split())
            # check if input is in range
            if not (MIN_64BIT_INT <= x <= MAX_64BIT_INT and MIN_64BIT_INT <= y <= MAX_64BIT_INT):
                continue
            live_cells.add((x, y))
        except (ValueError, IndexError):
            # Skip malformed lines
            continue

    return live_cells


def generate_life_106_string(live_cells: set) -> str:
    """
    :param live_cells: a set of tuples representing live cells in a conway's game of life simulation
    :return: string in Life 1.06 format
    """
    output_list = ["#Life 1.06"]

    # could sort cells for cleaner output, but inefficient if readability is not a factor
    # sorted_live_cells = sorted(list(live_cells))
    for x, y in live_cells:
        output_list.append(f"{x} {y}")

    return "\n".join(output_list)


def game_of_life(live_cells: set, generations: int = 10) -> set:
    """
    :param generations:
    :param live_cells: a set of tuples representing live cells in a conway's game of life simulation
    :return: a set of tuples representing live cells in a conway's game of life simulation after (10) generations
    """
    for _ in range(generations):
        # using defaultdict to avoid KeyErrors
        neighbor_counts = defaultdict(int)

        # increment the 8 neighbors for all live cells
        for x, y in live_cells:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # live cell is not its own neighbor
                    if i == 0 and j == 0:
                        continue
                    # only consider neighbors that are within the 64-bit space.
                    nx, ny = x + i, y + j
                    if MIN_64BIT_INT <= nx <= MAX_64BIT_INT and MIN_64BIT_INT <= ny <= MAX_64BIT_INT:
                        neighbor_counts[(nx, ny)] += 1
                    # neighbor_counts[(x + i, y + j)] += 1

        next_gen_live_cells = set()

        # calculate next generation based on rules of life
        for cell, neighbor_count in neighbor_counts.items():
            # birth rule: a dead cell with exactly 3 neighbors comes to life
            if cell not in live_cells and neighbor_count == 3:
                next_gen_live_cells.add(cell)
            # survival rule: a live cell with 2 or 3 neighbors survives
            elif cell in live_cells and (neighbor_count == 2 or neighbor_count == 3):
                next_gen_live_cells.add(cell)

        live_cells = next_gen_live_cells

    return live_cells

if __name__ == "__main__":
    import argparse
    import sys

    # define optional arguments
    parser = argparse.ArgumentParser(
        description="Run Conway's Game of Life. Defaults to reading from stdin."
    )
    parser.add_argument(
        '-f', '--file',
        dest='filepath',
        help="Path to the Life 1.06 file to use as input instead of stdin."
    )
    parser.add_argument(
        '-g', '--generations',
        type=int,
        default=10,
        help="Number of generations to run (default: 10)."
    )
    args = parser.parse_args()

    life_106_string = ""

    # check if --file argument was provided
    if args.filepath:
        try:
            with open(args.filepath, 'r') as f:
                life_106_string = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at '{args.filepath}'", file=sys.stderr)
            sys.exit(1)
    else:
        # if no filepath was given, read from standard input (stdin).
        life_106_string = sys.stdin.read()

    # --- The rest of your logic remains the same ---
    start_state = parse_life_106_string(life_106_string)
    end_state = game_of_life(start_state, generations=args.generations)
    end_106_string = generate_life_106_string(end_state)

    print(end_106_string.strip())

