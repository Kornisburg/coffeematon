import pytest

from coffeematon.automatons.int_automaton import InteractingAutomaton
from coffeematon.automatons.nonint_automaton import NonInteractingAutomaton
from coffeematon.encoding import Compression

try:
    from coffeematon.automatons.fluid_automaton import FluidAutomaton
except ModuleNotFoundError:
    FluidAutomaton = None


def test_int():
    automaton = InteractingAutomaton(
        10,
        save=False,
        workers=8,
        compression=Compression.GZIP,
    )
    automaton.simulate(n_steps=10)


def test_nonint():
    automaton = NonInteractingAutomaton(10, save=False)
    automaton.simulate(n_steps=10)


@pytest.mark.skipif(FluidAutomaton is None, reason="phi is not installed")
def test_fluid():
    automaton = FluidAutomaton(10, save=False)
    automaton.simulate(n_steps=10)


def test_int_circular():
    automaton = InteractingAutomaton(10, initial_state="circular", save=False)
    automaton.simulate(n_steps=10)


def test_nonint_circular():
    automaton = NonInteractingAutomaton(10, initial_state="circular", save=False)
    automaton.simulate(n_steps=10)


@pytest.mark.skipif(FluidAutomaton is None, reason="phi is not installed")
def test_fluid_circular():
    automaton = FluidAutomaton(10, initial_state="circular", save=False)
    automaton.simulate(n_steps=10)


def test_workers_are_clamped():
    automaton = InteractingAutomaton(10, save=False, workers=0)
    assert automaton.workers == 1


def test_effective_workers_adaptive():
    small = InteractingAutomaton(20, save=False, workers=8)
    large = InteractingAutomaton(100, save=False, workers=100)
    assert small.effective_workers == 1
    assert large.effective_workers == 10
