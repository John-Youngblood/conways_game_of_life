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
            if cell not in live_cells and neighbor_count == 3:
                next_gen_live_cells.add(cell)
            elif cell in live_cells and (neighbor_count == 2 or neighbor_count == 3):
                next_gen_live_cells.add(cell)

        live_cells = next_gen_live_cells

    return live_cells

if __name__ == "__main__":
    glider_start_106_string = """
#Life 1.06
1 0
2 1
0 2
1 2
2 2
"""
    print("--- Glider Initial State ---")
    print(glider_start_106_string.strip())

    glider_start_state = parse_life_106_string(glider_start_106_string)

    glider_end_state = game_of_life(glider_start_state, 10)

    glider_end_106_string = generate_life_106_string(glider_end_state)

    print("\n--- Glider State After 10 Iterations ---")
    print(glider_end_106_string.strip())

