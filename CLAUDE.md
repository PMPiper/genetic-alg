# genetic-alg

Genetic algorithm visualization in Python using tkinter. Dots evolve over generations to reach a goal.

## Structure

```
src/python/
  main.py        ← entry point; configures pop size, brain size, mutation rate
  population.py  ← Population class; manages generations, fitness, selection
  dot.py         ← Dot class; movement, fitness calculation, cloning/mutation
  brain.py       ← Brain class; DNA (list of direction tuples), randomize/mutate
```

## Commands

```bash
uv run python src/python/main.py   # run the simulation (opens tkinter window)
```

## Notes

- No external dependencies — stdlib only (tkinter, math, random, copy)
- Source files use direct module imports (`import dot`, `import brain`), so they must be run from `src/python/` or via `uv run python src/python/main.py`
- Canvas is 600×600; goal is a small oval near the top center
