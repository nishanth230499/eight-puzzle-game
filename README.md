# Eight Puzzle Game Solver

A Python-based program to solve the classic **Eight Puzzle Game** using different search heuristics. This project demonstrates AI search algorithms and allows users to explore their performance based on various metrics.

## Features

1. **Difficulty Level**
   - Users can select a difficulty level (0-7) or input their own initial state configuration.
2. **Heuristic Methods**  
   The game uses three heuristic approaches to find the solution:

   - **Misplaced Heuristic**: Counts the number of misplaced tiles compared to the goal state.
   - **Manhattan Heuristic**: Calculates the sum of Manhattan distances for each tile from its current position to the target position.
   - **Uniform Cost Search**: A search method without heuristics, purely exploring all possible moves.

3. **State Selection**  
   At each step, the algorithm evaluates the possible neighboring states and selects the most optimal state based on the heuristic.

4. **Performance Statistics**  
   Once the goal state is reached, the program outputs valuable statistics such as:

   - Solution depth
   - Running time
   - Number of nodes expanded
   - Maximum queue size during execution

5. **Heuristic Comparison**  
   This project allows easy comparison of the efficiency and performance of each heuristic method based on a given puzzle configuration.

## Usage

In the project directory, you can run:

### `python n_puzzle.py`

Then follow the prompts to choose your desired difficulty level (0-7) or provide a custom puzzle configuration. The program will compute the solution and display detailed performance statistics for each of the heuristics.

## Future Enhancements

- Extend UI to visualize puzzles and their solutions.
- Add support for real-time heuristic selection and switching during execution.
- Implement optimizations for larger puzzles (e.g., 15-puzzle, 24-puzzle).
