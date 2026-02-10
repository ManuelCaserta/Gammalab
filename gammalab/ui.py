"""
UI helper functions for Streamlit interface.

This module contains reusable UI components and visualization helpers.
"""

import plotly.graph_objects as go
import numpy as np
from typing import Dict


_DARK_LAYOUT_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="#050807",
    plot_bgcolor="#050807",
    font=dict(color="#e7ffe7"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#e7ffe7")),
)


def _axis_dark(title: str):
    return dict(
        title=title,
        gridcolor="#123321",
        zerolinecolor="#123321",
        tickcolor="#123321",
        linecolor="#123321",
        showline=True,
    )


def plot_transmission_vs_thickness(
    material_key: str,
    energy_mev: float,
    max_thickness_mm: float,
    current_thickness_mm: float,
    transmission_func
) -> go.Figure:
    """
    Create a plotly figure showing transmission I/I0 vs thickness.
    
    Args:
        material_key: Material identifier
        energy_mev: Photon energy in MeV
        max_thickness_mm: Maximum thickness for plot range (mm)
        current_thickness_mm: Current selected thickness (mm) - shown as marker
        transmission_func: Function to calculate transmission (material_key, energy, thickness_cm)
        
    Returns:
        Plotly figure object
    """
    # Generate thickness array in mm, convert to cm for calculation
    thickness_mm = np.linspace(0, max_thickness_mm, 200)
    thickness_cm = thickness_mm / 10.0
    
    # Calculate transmission for each thickness
    transmissions = [
        transmission_func(material_key, energy_mev, t_cm)
        for t_cm in thickness_cm
    ]
    
    fig = go.Figure()
    
    # Curva principale
    fig.add_trace(go.Scatter(
        x=thickness_mm,
        y=transmissions,
        mode='lines',
        name='Trasmissione I/I₀',
        line=dict(color='#00cc55', width=2),
        hovertemplate='Spessore: %{x:.2f} mm<br>Trasmissione: %{y:.4f}<extra></extra>'
    ))
    
    # Marcatore valore attuale
    current_thickness_cm = current_thickness_mm / 10.0
    current_transmission = transmission_func(material_key, energy_mev, current_thickness_cm)
    fig.add_trace(go.Scatter(
        x=[current_thickness_mm],
        y=[current_transmission],
        mode='markers',
        name='Valore attuale',
        marker=dict(color='#00ff66', size=12, symbol='circle', line=dict(color="#e7ffe7", width=1)),
        hovertemplate='Attuale: %{x:.2f} mm, I/I₀ = %{y:.4f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Trasmissione vs spessore",
        yaxis=dict(range=[0, 1.05]),
        hovermode='x unified',
        showlegend=True,
        legend=dict(x=0.02, y=0.98)
    )
    fig.update_layout(**_DARK_LAYOUT_BASE)
    fig.update_xaxes(**_axis_dark("Spessore (mm)"))
    fig.update_yaxes(**_axis_dark("Trasmissione I/I₀"), range=[0, 1.05])
    
    return fig


def plot_interaction_probabilities(probabilities: Dict[str, float], energy_mev: float) -> go.Figure:
    """
    Create a bar chart showing interaction probabilities.
    
    Args:
        probabilities: Dictionary with keys "photoelectric", "compton", "pair"
        energy_mev: Photon energy in MeV (for threshold annotation)
        
    Returns:
        Plotly figure object
    """
    labels = ['Fotoelettrico', 'Compton', 'Produzione di coppie']
    values = [
        probabilities['photoelectric'],
        probabilities['compton'],
        probabilities['pair']
    ]
    colors = ['#00ff66', '#00cc55', '#009944']
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=[f'{v:.1%}' for v in values],
            textposition='outside',
            hovertemplate='%{x}<br>Probabilità: %{y:.4f} (%{text})<extra></extra>'
        )
    ])
    
    annotations = []
    if energy_mev < 1.022 and probabilities['pair'] == 0:
        annotations.append(dict(
            x=2,
            y=0.05,
            text="La produzione di coppie avviene<br>solo sopra la soglia 1,022 MeV",
            showarrow=False,
            font=dict(size=10, color='gray'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray',
            borderwidth=1
        ))
    
    fig.update_layout(
        title="Probabilità di interazione",
        yaxis=dict(range=[0, 1.1]),
        annotations=annotations
    )
    fig.update_layout(**_DARK_LAYOUT_BASE)
    fig.update_xaxes(**_axis_dark(""))
    fig.update_yaxes(**_axis_dark("Probabilità"), range=[0, 1.1])
    
    return fig


def plot_monte_carlo_results(results: Dict) -> go.Figure:
    """
    Create a pie chart showing Monte Carlo simulation outcomes.
    
    Args:
        results: Dictionary from run_monte_carlo with counts and fractions
        
    Returns:
        Plotly figure object
    """
    labels = ['Trasmessi', 'Fotoelettrico', 'Compton', 'Produzione di coppie']
    values = [
        results['transmitted'],
        results['photoelectric_count'],
        results['compton_count'],
        results['pair_count']
    ]
    colors = ['#00ff66', '#00cc55', '#009944', '#007733']
    
    filtered_data = [(l, v, c) for l, v, c in zip(labels, values, colors) if v > 0]
    if not filtered_data:
        filtered_data = [(l, v, c) for l, v, c in zip(labels, values, colors)]
    
    labels_filtered, values_filtered, colors_filtered = zip(*filtered_data)
    
    fig = go.Figure(data=[go.Pie(
        labels=labels_filtered,
        values=values_filtered,
        marker_colors=colors_filtered,
        textinfo='label+percent+value',
        hovertemplate='%{label}<br>Conteggio: %{value}<br>Percentuale: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=f"Risultati Monte Carlo (N = {results['n_photons']:,})",
    )
    fig.update_layout(**_DARK_LAYOUT_BASE)
    
    return fig


def plot_monte_carlo_interactions(results: Dict) -> go.Figure:
    """
    Create a bar chart showing interaction type counts from Monte Carlo.
    
    Args:
        results: Dictionary from run_monte_carlo with counts
        
    Returns:
        Plotly figure object
    """
    labels = ['Fotoelettrico', 'Compton', 'Produzione di coppie']
    values = [
        results['photoelectric_count'],
        results['compton_count'],
        results['pair_count']
    ]
    colors = ['#00ff66', '#00cc55', '#009944']
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=[f'{v:,}' if v > 0 else '' for v in values],
            textposition='outside',
            hovertemplate='%{x}<br>Conteggio: %{y:,}<br>Frazione: %{customdata:.2%}<extra></extra>',
            customdata=[results['photoelectric_fraction'], 
                       results['compton_fraction'], 
                       results['pair_fraction']]
        )
    ])
    
    fig.update_layout(
        title="Conteggi per tipo di interazione",
    )
    fig.update_layout(**_DARK_LAYOUT_BASE)
    fig.update_xaxes(**_axis_dark(""))
    fig.update_yaxes(**_axis_dark("Conteggio"))
    
    return fig


def plot_transmission_vs_energy(
    material_key: str,
    thickness_mm: float,
    transmission_func
) -> go.Figure:
    """
    Plot transmission I/I0 versus energy for a fixed thickness.

    Args:
        material_key: Material identifier.
        thickness_mm: Fixed thickness in mm.
        transmission_func: Callable(material_key, energy_mev, thickness_cm).
    """
    energies = np.linspace(0.05, 10.0, 240)
    thickness_cm = thickness_mm / 10.0
    transmissions = [transmission_func(material_key, float(e), thickness_cm) for e in energies]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=energies,
            y=transmissions,
            mode="lines",
            line=dict(color="#00cc55", width=2),
            name="Trasmissione I/I₀",
            hovertemplate="Energia: %{x:.3f} MeV<br>Trasmissione: %{y:.4f}<extra></extra>",
        )
    )
    fig.add_vline(
        x=1.022,
        line_dash="dash",
        line_color="#d62728",
        annotation_text="Soglia coppie 1,022 MeV",
        annotation_position="top right",
    )
    fig.update_layout(
        title=f"Trasmissione vs energia (spessore = {thickness_mm:.2f} mm)",
        yaxis=dict(range=[0, 1.05]),
    )
    fig.update_layout(**_DARK_LAYOUT_BASE)
    fig.update_xaxes(**_axis_dark("Energia fotone (MeV)"))
    fig.update_yaxes(**_axis_dark("Trasmissione I/I₀"), range=[0, 1.05])
    return fig

