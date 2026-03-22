"""Entry point for the genetic algorithm dot simulation."""

import time
import tkinter

import population


def main() -> None:
    """Runs the genetic algorithm simulation."""
    tk = tkinter.Tk()
    pop = population.Population(
        pop_tk=tk,
        pop_size=15,
        brain_size=75,
        mutation_rate=0.1,
    )
    pop.make_first_pop()
    pop.run_generation()
    time.sleep(2)

    for _ in range(15):
        if pop.goal_reached:
            break
        pop.new_population()
        pop.run_generation()
        time.sleep(2)

    tk.mainloop()


if __name__ == "__main__":
    main()
