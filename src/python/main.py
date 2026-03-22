"""Entry point for the genetic algorithm dot simulation."""

import argparse
import time
import tkinter

import population


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments for the simulation.

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="Genetic algorithm dot simulation.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--pop-size",
        type=int,
        default=15,
        metavar="N",
        help="Dots per generation.",
    )
    parser.add_argument(
        "--brain-size",
        type=int,
        default=400,
        metavar="N",
        help="Steps per dot brain.",
    )
    parser.add_argument(
        "--mutation-rate",
        type=float,
        default=0.01,
        metavar="F",
        help="Probability any DNA step mutates on reproduction.",
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=50,
        metavar="N",
        help="Maximum generations to run.",
    )
    parser.add_argument(
        "--num-parents",
        type=int,
        default=5,
        metavar="N",
        help=(
            "Top-N parents selected for breeding each generation. "
            "Values > 1 preserve diversity; with N=1 only the best dot "
            "ever breeds (random local search, not a true GA)."
        ),
    )
    parser.add_argument(
        "--crossover",
        action="store_true",
        help=(
            "Enable single-point DNA crossover between two roulette-selected "
            "parents. Has no effect when --num-parents is 1."
        ),
    )
    parser.add_argument(
        "--fitness-mode",
        choices=["distance", "waypoint"],
        default="waypoint",
        help=(
            "'distance': 1/straight-line-distance² — simple but misleading "
            "when an obstacle blocks the direct path. "
            "'waypoint': routes the measured distance around the obstacle "
            "when the dot is on the far side, giving a gradient that points "
            "toward a reachable path."
        ),
    )
    parser.add_argument(
        "--penalize-obstacle-death",
        action="store_true",
        help="Halve the fitness of any dot that died by hitting the obstacle.",
    )
    return parser.parse_args()


def main() -> None:
    """Runs the genetic algorithm simulation."""
    args = parse_args()

    tk = tkinter.Tk()
    pop = population.Population(
        pop_tk=tk,
        pop_size=args.pop_size,
        brain_size=args.brain_size,
        mutation_rate=args.mutation_rate,
        num_parents=args.num_parents,
        use_crossover=args.crossover,
        fitness_mode=args.fitness_mode,
        penalize_obstacle_death=args.penalize_obstacle_death,
    )
    pop.make_first_pop()
    pop.run_generation()
    time.sleep(2)

    for _ in range(args.generations):
        if pop.goal_reached:
            break
        pop.new_population()
        pop.run_generation()
        time.sleep(2)

    tk.mainloop()


if __name__ == "__main__":
    main()
