# Rubik's Cube Solver

This project provides a framework to solve a Rubik's Cube through multiple heuristics and search algorithms. The `RubikSolver` class implements various methods for solving the cube, including **Breadth-First Search (BFS)** and heuristic-based approaches. Heuristics include Hamming distance, path length, and custom edge and corner alignment checks. The `RubikCube` class defines the cube structure and allows for various rotations, shuffles, and move sequences.

## Features

- **Cube Representation**: A `RubikCube` class that represents a 3D array of the cube’s faces and includes methods for manipulating the cube.
- **Heuristics**: Implemented within the `Heuristics` class, several heuristics allow the solver to estimate the number of moves to solve the cube:
  - **Hamming Distance**: Measures how many pieces differ from their solved positions.
  - **Path Length Heuristic**: Uses the path length as a heuristic.
  - **Cross and Corner Alignments**: Checks central and corner alignments on the cube to assess partial solutions.
- **Node Management**: Node classes (`Node`, `Node_A_Star`, and `HeuristicNode`) track the cube state and solution path.
- **Movement Methods**: The `RubikCube` class includes functions to perform movements along each axis:
  - **Horizontal, Vertical, and Z-Axis** moves are implemented to simulate realistic rotations.
  - `shuffle` functions allow random shuffles with or without opposite move prevention.
- **Solving Algorithms**: The `RubikSolver` class includes a **Breadth-First Search (BFS)** implementation and can be extended with other search techniques.

## Code Structure

### Classes and Key Methods

1. **`Heuristics`**:
   - `hamming_distance(node_a, node_b)`: Counts pieces out of place.
   - `heuristic3(node1, node2)`: Uses path length as a heuristic.
   - `cruz(node1, node2)`: Checks central alignment of horizontal and vertical cube faces.
   - `esquinas(node1, node2)`: Evaluates corner alignment, rewarding correct positions.

2. **`Node`, `Node_A_Star`, `HeuristicNode`**:
   - Represent different nodes in search trees with attributes such as `path`, `distance`, and heuristic values.
   - Overload comparison operators to facilitate priority in queues for search.

3. **`RubikCube`**:
   - Initializes the cube as a solved structure with six faces, each with a unique color.
   - **Rotation Methods**:
      - `__horizontal_right(row, face_rotate)`: Moves rows horizontally.
      - `__vertical_up(col, face_rotate)`: Moves columns vertically.
      - `__z_right(z_col, face_rotate)`: Rotates around the Z-axis.
   - **Shuffle Methods**:
      - `shuffle(N)`: Randomly shuffles the cube with possible repetition.
      - `shuffle_unrepeat(N)`: Ensures non-repetitive shuffling by avoiding immediate reverse moves.
   - **Other Methods**:
      - `move_list(moves_list)`: Executes a list of specified moves to bring the cube to a desired state.

4. **`RubikSolver`**:
   - `breadth_first_search()`: A breadth-first approach to find the solution without heuristics.
   - `INF`: Represents an infinite distance value for search algorithms.

## Getting Started

### Prerequisites
- Python 3.7+
- `numpy` library

### Installation

Install `numpy` by running:
```bash
pip install numpy
