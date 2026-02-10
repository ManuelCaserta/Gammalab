"""Unit tests for UI plot builders."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("plotly")

from gammalab.models import transmission_fraction
from gammalab.ui import (
    plot_interaction_probabilities,
    plot_monte_carlo_interactions,
    plot_monte_carlo_results,
    plot_transmission_vs_energy,
    plot_transmission_vs_thickness,
)


def test_plot_transmission_vs_thickness_structure() -> None:
    fig = plot_transmission_vs_thickness("H2O", 1.0, 50.0, 5.0, transmission_fraction)
    assert len(fig.data) == 2  # curve + current marker
    assert fig.data[0].mode == "lines"
    assert fig.data[1].mode == "markers"
    assert fig.layout.yaxis.range[0] == 0


def test_plot_interaction_probabilities_data() -> None:
    probs = {"photoelectric": 0.2, "compton": 0.5, "pair": 0.3}
    fig = plot_interaction_probabilities(probs, 2.0)
    bar = fig.data[0]
    assert list(bar.y) == [0.2, 0.5, 0.3]
    assert abs(sum(bar.y) - 1.0) < 1e-12


def test_plot_monte_carlo_results_contains_nonzero_slices() -> None:
    results = {
        "n_photons": 10000,
        "transmitted": 6000,
        "photoelectric_count": 2000,
        "compton_count": 1500,
        "pair_count": 500,
    }
    fig = plot_monte_carlo_results(results)
    assert len(fig.data) == 1
    pie = fig.data[0]
    assert int(np.sum(pie.values)) == 10000


def test_plot_monte_carlo_interactions_values() -> None:
    results = {
        "photoelectric_count": 120,
        "compton_count": 300,
        "pair_count": 80,
        "photoelectric_fraction": 0.24,
        "compton_fraction": 0.60,
        "pair_fraction": 0.16,
    }
    fig = plot_monte_carlo_interactions(results)
    bar = fig.data[0]
    assert list(bar.y) == [120, 300, 80]


def test_plot_transmission_vs_energy_bounds() -> None:
    fig = plot_transmission_vs_energy("H2O", 10.0, transmission_fraction)
    assert len(fig.data) == 1
    curve = fig.data[0]
    assert curve.x[0] >= 0.05
    assert curve.x[-1] <= 10.0

