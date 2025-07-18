package main

import (
	"fmt"
	"strconv"
	"math"
	"io"
    "os"
	"strings"
)

const (
	MinInt64 = math.MinInt64
	MaxInt64 = math.MaxInt64
)

// Cell contains the X, Y coordinates of a cell in a conways game of life simulation.
type Cell struct {
	X, Y int
}

func ParseLife106String(life106String string) (map[Cell]struct{}, error) {
	/*
		:param life106String: string in Life 1.06 format
		:return: a slice of Cells representing live cells in a conway's game of life simulation
	*/
	lines := strings.Split(strings.TrimSpace(life106String), "\n")
	// check for Life 1.06 header
	if len(lines) == 0 || lines[0] != "#Life 1.06" {
		return nil, fmt.Errorf("invalid Life 1.06 format: missing or incorrect header")
	}

	liveCells := make(map[Cell]struct{})
	for _, line := range lines[1:] {
		parts := strings.Fields(line)
		// check that we have 2 values in each line
		if len(parts) != 2 {
			continue
		}
		x, errX := strconv.Atoi(parts[0])
		y, errY := strconv.Atoi(parts[1])
		// check that both values are ints and within signed 64 bit range
		if errX != nil || errY != nil {
			continue
		}
		liveCells[Cell{X: x, Y: y}] = struct{}{}
	}
	return liveCells, nil
}

func GenerateLife106String(liveCells map[Cell]struct{}) string {
	/*
			:param live_cells: a slice of Cells representing live cells in a conway's game of life simulation
		    :return: string in Life 1.06 format
	*/
	// initialize slice with Life 1.06 header
	lines := []string{"#Life 1.06"}

	// convert each cell to a string and add to slice
	for cell := range liveCells {
		lines = append(lines, fmt.Sprintf("%d %d", cell.X, cell.Y))
	}

	// join all strings in lines into a single string
	return strings.Join(lines, "\n")
}

func GameOfLife(liveCells map[Cell]struct{}, generations int) map[Cell]struct{} {
	/*
		:param live_cells: a set of tuples representing live cells in a conway's game of life simulation
		:param generations: number of generations of conways game of life to iterate through
		:return: a slice of Cells representing live cells in a conway's game of life simulation after (10) generations
	*/

	// iterate through each generation
	for i := 0; i < generations; i++ {
		neighborCounts := make(map[Cell]int)

		// increment neighbors for all live cells
		for cell := range liveCells {
			for dx := -1; dx <= 1; dx++ {
				for dy := -1; dy <= 1; dy++ {
					// live cell is not its own neighbor
					if dx == 0 && dy == 0 {
						continue
					}

                    // check if neighbor is out of range
                    if (dx > 0 && cell.X > MaxInt64-dx) || (dx < 0 && cell.X < MinInt64-dx) {
						continue
					}
					if (dy > 0 && cell.Y > MaxInt64-dy) || (dy < 0 && cell.Y < MinInt64-dy) {
						continue
					}
					neighbor := Cell{X: cell.X + dx, Y: cell.Y + dy}
					neighborCounts[neighbor]++
				}
			}
		}

		nextGenLiveCells := make(map[Cell]struct{})

		// apply the rules of life
		for cell, count := range neighborCounts {
			_, isAlive := liveCells[cell] // check if the cell is currently alive

			// birth rule: a dead cell with exactly 3 neighbors comes to life
			if !isAlive && count == 3 {
				nextGenLiveCells[cell] = struct{}{}
			}

			// survival rule: a live cell with 2 or 3 neighbors survives
			if isAlive && (count == 2 || count == 3) {
				nextGenLiveCells[cell] = struct{}{}
			}
		}
		liveCells = nextGenLiveCells
	}

	return liveCells
}

func main() {
    // parse stdin
	inputBytes, err := io.ReadAll(os.Stdin)
    if err != nil {
        fmt.Println("Error reading from stdin:", err)
        return
    }
    life106String := string(inputBytes)

    // convert life_106_string to start state slice
    gliderStartState, err := ParseLife106String(life106String)
    if err != nil {
       fmt.Println("Error parsing start state:", err)
       return
    }

    //  run game of life for 10 generations
    gliderEndState := GameOfLife(gliderStartState, 10)

    // convert end state slice to life_106_string
    gliderEndString := GenerateLife106String(gliderEndState)

    fmt.Println(gliderEndString)
}
