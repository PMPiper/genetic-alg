# genetic-alg

Visualization of a genetic algorithm. Dots evolve over generations, each following a randomly generated sequence of steps, selecting for those that get closest to the goal.

Adapted from [Code Bullet's Smart Dots tutorial](https://github.com/Code-Bullet/Smart-Dots-Genetic-Algorithm-Tutorial).

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- tkinter (not bundled on Ubuntu/WSL — install separately):
  ```bash
  sudo apt install python3-tk
  ```

## Setup

```bash
git clone git@github.com:PMPiper/genetic-alg.git
cd genetic-alg
uv sync
```

## Run

```bash
uv run python src/python/main.py
```

Opens a 600×600 tkinter window. Dots start in the centre and attempt to reach the green goal near the top.

## Parameters

Edit `src/python/main.py` to adjust:

| Parameter | Default | Effect |
|---|---|---|
| `pop_size` | `15` | Dots per generation |
| `brain_size` | `75` | Steps each dot takes per generation |
| `mutation_rate` | `0.1` | Probability any step is randomised on mutation |

The number of generations is controlled by the `range()` value in the `for` loop in `main.py`. Increasing `pop_size` or `brain_size` will affect performance.
