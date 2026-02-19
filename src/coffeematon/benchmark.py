"""Lightweight benchmark harness for multithread/coarse-grain complexity pipeline."""

import argparse
from statistics import mean
from time import perf_counter

from coffeematon.automatons.int_automaton import InteractingAutomaton
from coffeematon.encoding import Compression


def run_once(n: int, steps: int, workers: int, compression: str) -> float:
    automaton = InteractingAutomaton(
        n,
        save=False,
        workers=workers,
        compression=compression,
    )
    start = perf_counter()
    automaton.simulate(n_steps=steps, max_save_steps=steps)
    return perf_counter() - start


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=100)
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--workers", type=int, nargs="+", default=[1, 2, 4, 8])
    parser.add_argument(
        "--compression",
        choices=[c.value for c in Compression],
        default=Compression.GZIP.value,
    )
    args = parser.parse_args()

    print(
        f"Benchmark: n={args.n}, steps={args.steps}, repeats={args.repeats}, compression={args.compression}"
    )
    for workers in args.workers:
        timings = [
            run_once(args.n, args.steps, workers, args.compression)
            for _ in range(args.repeats)
        ]
        print(
            f"workers={workers:>2} | avg={mean(timings):.3f}s | min={min(timings):.3f}s | max={max(timings):.3f}s"
        )


if __name__ == "__main__":
    main()
