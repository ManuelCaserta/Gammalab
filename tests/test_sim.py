"""Unit tests for Monte Carlo simulation module."""

from __future__ import annotations

import math

import pytest

from gammalab.sim import run_monte_carlo


def test_monte_carlo_reproducibility_with_seed() -> None:
    """Same seed and same inputs must produce identical counts."""
    result_a = run_monte_carlo("H2O", 1.0, 1.0, 20000, seed=1234)
    result_b = run_monte_carlo("H2O", 1.0, 1.0, 20000, seed=1234)
    assert result_a == result_b


def test_monte_carlo_different_seeds_change_outcome() -> None:
    """Different seeds should typically produce different outcomes."""
    result_a = run_monte_carlo("H2O", 1.0, 1.0, 3000, seed=11)
    result_b = run_monte_carlo("H2O", 1.0, 1.0, 3000, seed=12)
    assert result_a["transmitted"] != result_b["transmitted"] or result_a["interactions"] != result_b["interactions"]


def test_monte_carlo_statistical_accuracy() -> None:
    """Simulated transmission should be close to analytical transmission."""
    n_photons = 100_000
    result = run_monte_carlo("H2O", 1.0, 1.5, n_photons, seed=7)
    simulated = result["transmitted_fraction"]
    analytical = result["analytical_transmission"]
    # 4 sigma binomial margin (conservative educational threshold)
    sigma = math.sqrt(analytical * (1.0 - analytical) / n_photons)
    assert abs(simulated - analytical) <= 4.0 * sigma + 0.002


def test_monte_carlo_zero_thickness_all_transmitted() -> None:
    """At zero thickness, all photons should transmit."""
    result = run_monte_carlo("Pb", 0.5, 0.0, 5000, seed=10)
    assert result["transmitted"] == 5000
    assert result["interactions"] == 0
    assert result["transmitted_fraction"] == 1.0


def test_monte_carlo_low_energy_no_pair() -> None:
    """Below 1.022 MeV pair count must be zero."""
    result = run_monte_carlo("Pb", 1.0, 5.0, 40000, seed=8)
    assert result["pair_count"] == 0


def test_monte_carlo_invalid_inputs() -> None:
    """Simulation should validate n_photons and thickness."""
    with pytest.raises(ValueError):
        run_monte_carlo("H2O", 1.0, 1.0, 0, seed=1)
    with pytest.raises(ValueError):
        run_monte_carlo("H2O", 1.0, -1.0, 1000, seed=1)

