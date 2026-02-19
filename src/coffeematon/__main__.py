"""
Collecting automaton output
"""

import argparse
from time import time
from typing import Dict, Optional, Type

import numpy

from coffeematon.automatons.automaton import Automaton, ArrayTypes, InitialStates
from coffeematon.automatons.int_automaton import InteractingAutomaton
from coffeematon.automatons.nonint_automaton import NonInteractingAutomaton
from coffeematon.encoding import Compression
from coffeematon.plot_results import plot_results

try:
    from coffeematon.automatons.fluid_automaton import FluidAutomaton
except ModuleNotFoundError:
    FluidAutomaton = None


AUTOMATONS: Dict[str, Type[Automaton]] = {
    "nonint": NonInteractingAutomaton,
    "int": InteractingAutomaton,
}
if FluidAutomaton is not None:
    AUTOMATONS["fluid"] = FluidAutomaton


def experiment_for_n(
    automaton_type: str,
    n: int,
    init: Optional[InitialStates] = None,
    save: bool = True,
    workers: Optional[int] = None,
    compression: str = Compression.GZIP.value,
):
    automaton_class = AUTOMATONS[automaton_type]
    automaton: Automaton = automaton_class(
        n,
        init,
        save=save,
        workers=workers,
        compression=compression,
    )

    t_start = time()
    csv_results_path = automaton.simulate()
    t_end = time()
    print(f"Time for n={automaton.n}: {t_end - t_start:.2E} sec.")

    plot_results(csv_results_path)

    mix_time = automaton.step
    emax_val = max(automaton.complexities[ArrayTypes.FINE])
    cmax_time = automaton.steps[
        numpy.argmax(automaton.complexities[ArrayTypes.COARSE_7])
    ]
    cmax_val = max(automaton.complexities[ArrayTypes.COARSE_7])
    return (mix_time, emax_val, cmax_time, cmax_val)


def data_for_range(type, start, stop, step=1):
    ns = range(start, stop, step)
    mix_times = []
    emax_vals = []
    cmax_times = []
    cmax_vals = []

    t1 = time()
    for n in ns:
        (mix_time, emax_val, cmax_time, cmax_val) = experiment_for_n(type, n)
        mix_times.append(mix_time)
        emax_vals.append(emax_val)
        cmax_times.append(cmax_time)
        cmax_vals.append(cmax_val)
    t2 = time()
    print(f"Total time: {t2 - t1:d} sec.")

    f = open("stats_%s_%d_%d" % (type, start, stop - step), "w")
    f.write("ns = " + str(ns) + "\n")
    f.write("mix_times = " + str(mix_times) + "\n")
    f.write("emax_vals = " + str(emax_vals) + "\n")
    f.write("cmax_times = " + str(cmax_times) + "\n")
    f.write("cmax_vals = " + str(cmax_vals) + "\n")
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--automaton",
        choices=AUTOMATONS.keys(),
        help="Type of automaton to use.",
        required=True,
    )
    parser.add_argument(
        "-n",
        help="Size of the automaton.",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--init",
        help="Initial state of the automaton.",
        choices=[i.value for i in InitialStates],
        default="updown",
    )
    parser.add_argument(
        "--workers",
        type=int,
        help="Number of worker threads used to compute compressed sizes.",
        default=None,
    )
    parser.add_argument(
        "--compression",
        choices=[c.value for c in Compression],
        default=Compression.GZIP.value,
        help="Compression backend used for complexity estimation.",
    )
    args = parser.parse_args()
    experiment_for_n(
        args.automaton,
        args.n,
        args.init,
        workers=args.workers,
        compression=args.compression,
    )


if __name__ == "__main__":
    main()
