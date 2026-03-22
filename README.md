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

```bash
uv run python src/python/main.py --help
```
