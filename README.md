# TSP Optimization with Tabu Search and Simulated Annealing

Two standalone Python implementations of local-search metaheuristics for the
Travelling Salesman Problem (TSP):

- **Tabu Search** with a 2-opt neighbourhood and a tabu list of recent moves.
- **Simulated Annealing** with random segment shuffling and Metropolis acceptance.

Both programs use the same 20-city instance, print the initial and final tour length,
and draw a live tour plus a convergence plot with Matplotlib.

This was an Artificial Intelligence course project at FIIT STU in Bratislava.

## Algorithms

### Tabu Search (`tabu_search.py`)

- Starts from a random permutation of the cities.
- Evaluates 2-opt moves that reverse a segment of the tour.
- Keeps a tabu list of the last moves; a move is released after 10 generations.
- Tracks the best tour found so far and the current tour separately.
- Uses a best-improvement-style scan over all 2-opt pairs.

### Simulated Annealing (`simulated_annealing.py`)

- Starts from a random permutation.
- Generates a neighbour by shuffling a random segment of the tour.
- Accepts improvements always and worse solutions with probability
  `exp(-delta / T)`.
- Starts at `T = 10000`, cools with `alpha = 0.995`, and performs 2500 sweeps.
- Keeps the best tour seen independently of the current tour.

## Project layout

```text
tabu_search.py           tabu search implementation
simulated_annealing.py   simulated annealing implementation
requirements.txt
```

The 20 city coordinates and the distance matrix are embedded in each script, so no
external data file is needed.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python tabu_search.py
python simulated_annealing.py
```

Each script opens two visual outputs: the current/best tour and a convergence chart.
Because the initial tour is random, the final distance varies between runs.

## Notes

- The scripts are intentionally standalone; they do not share a helper module.
- The neighbourhood and cooling parameters are defined at the top of each file and are
  easy to change for experiments.
- The convergence plot shows both the current solution and the best-so-far solution.

## Author

Ondrej Nebus - FIIT STU, Bratislava.
