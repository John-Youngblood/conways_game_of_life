# Conways Game of Life

This project is for answering the following prompt:

> ## Game of Life Prompt
> Implement [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in 64-bit signed integer space.
> 
> Imagine a 2D grid - each cell (coordinate) can be either "alive" or "dead". Every generation of the simulation, the system ticks forward. Each cell's value changes according to the following:
> 
> If an "alive" cell had less than 2 or more than 3 alive neighbors (in any of the 8 surrounding cells), it becomes dead.
> If a "dead" cell had *exactly* 3 alive neighbors, it becomes alive.
> Your input is a list of integer coordinates for live cells in the Life 1.06 format. They could be anywhere in the signed 64-bit range. This means the board could be very large!
> 
> Sample input:
> ```
> #Life 1.06
> 0 1
> 1 2
> 2 0
> 2 1
> 2 2
> -2000000000000 -2000000000000
> -2000000000001 -2000000000001
> -2000000000000 -2000000000001
> ```
> 
> Your program should read the state of the simulation from standard input, run 10 iterations of the Game of Life, and print the result to standard output in Life 1.06 format.
> 
> Please don’t spend more than 3 hours on your solution. Feel free to allocate that time in a manner that works best for your schedule. You may work in any language you prefer.
> 
> We're most interested in both the technical aspects of how you deal with very large integers and how you go about solving the problem. At the onsite, be prepared to discuss your solution, including the choices and tradeoffs you made. Though not required, you are welcome to bring a laptop with you to your interview to walk us through the code.

---
## Relevant Files

- `conways_game_of_life.py`: python implementation of prompt
- `conways_game_of_life.ipynb`: jupyter notebook used for prototyping out python implementation (also includes alternate convolution method)
- `requirements.txt`: necessary libraries for running jupyter notebook (not needed for running `conways_game_of_life.py`)
- `main.go`: go implementation (converted from python implementation with assistance from AI)

---
## How to Run
### Python Implementation
Pass input through stdin:
```bash
python conways_game_of_life.py << EOF
#Life 1.06
1 0
2 1
0 2
1 2
2 2
EOF
```
or using pipe:
```bash
cat glider.life | python conways_game_of_life.py
```
or using the `-f` flag:
```bash
python conways_game_of_life.py -f glider.life
```

you can also pass # of generations to go through using the `-g` flag (default 10):
```bash
python conways_game_of_life.py -f glider.life -g 50
```

to see all available options, use the `--help` flag:

```bash
python conways_game_of_life.py --help
```

### Go Implementation
build executable first:
```bash
go build
```

then pass input through stdin:
```bash
./goImplementation << EOF
#Life 1.06
1 0
2 1
0 2
1 2
2 2
EOF
```
or using pipe:
```bash
cat glider.life | ./goImplementation
```