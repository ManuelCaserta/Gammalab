"""
GammaLab - Punto di ingresso Streamlit

Simulatore didattico di attenuazione dei raggi gamma e meccanismi di interazione.
"""

import streamlit as st
import pandas as pd
from gammalab import models
from gammalab import sim
from gammalab.ui import (
    plot_interaction_probabilities,
    plot_monte_carlo_interactions,
    plot_monte_carlo_results,
    plot_transmission_vs_energy,
    plot_transmission_vs_thickness,
)
from gammalab import export

# Configurazione pagina
st.set_page_config(
    page_title="GammaLab",
    page_icon="assets/gammalab_icon.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Tema dark (nero) con risalti in verde + componenti più puliti
st.markdown(
    """
<style>
  :root{
    --gl-bg:#050807;
    --gl-panel:#0a120e;
    --gl-panel-2:#07100c;
    --gl-border:#123321;
    --gl-text:#e7ffe7;
    --gl-muted:#a6c6a6;
    --gl-accent:#00ff66;
    --gl-accent-2:#00cc55;
  }

  .stApp{ background-color: var(--gl-bg); color: var(--gl-text); }
  /* Evita che la parte alta venga coperta dalla top bar di Streamlit */
  .block-container{ padding-top: 2.75rem; padding-bottom:2rem; max-width: 1500px; }
  header[data-testid="stHeader"]{ background: transparent; }
  div[data-testid="stToolbar"]{ right: 0.75rem; }

  section[data-testid="stSidebar"], div[data-testid="stSidebar"]{
    background-color: var(--gl-panel-2) !important;
    border-right:1px solid var(--gl-border) !important;
  }
  /* Copre anche il contenitore interno della sidebar (Streamlit cambia spesso struttura DOM) */
  section[data-testid="stSidebar"] > div,
  div[data-testid="stSidebar"] > div{
    background-color: var(--gl-panel-2) !important;
  }
  hr{ margin:1.75rem 0 !important; border-color: var(--gl-border) !important; }
  a{ color: var(--gl-accent); }

  h1, h2, h3{ color: var(--gl-text); }
  h2, h3{ margin-top: 1.25rem !important; }

  /* Sidebar: controlli più leggibili e coerenti */
  section[data-testid="stSidebar"] .stMarkdown,
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] p,
  div[data-testid="stSidebar"] .stMarkdown,
  div[data-testid="stSidebar"] label,
  div[data-testid="stSidebar"] p { color: var(--gl-text) !important; }

  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3,
  div[data-testid="stSidebar"] h2,
  div[data-testid="stSidebar"] h3 { color: var(--gl-accent) !important; }

  section[data-testid="stSidebar"] hr,
  div[data-testid="stSidebar"] hr { border-color: var(--gl-border) !important; margin: 1.25rem 0 !important; }

  /* input/select/number */
  section[data-testid="stSidebar"] input,
  section[data-testid="stSidebar"] textarea,
  section[data-testid="stSidebar"] div[role="combobox"],
  div[data-testid="stSidebar"] input,
  div[data-testid="stSidebar"] textarea,
  div[data-testid="stSidebar"] div[role="combobox"]{
    background-color: var(--gl-panel) !important;
    color: var(--gl-text) !important;
    border: 1px solid var(--gl-border) !important;
    border-radius: 10px !important;
  }
  section[data-testid="stSidebar"] input:focus,
  section[data-testid="stSidebar"] textarea:focus,
  div[data-testid="stSidebar"] input:focus,
  div[data-testid="stSidebar"] textarea:focus{
    border-color: rgba(0,255,102,0.85) !important;
    box-shadow: 0 0 0 2px rgba(0,255,102,0.18) !important;
  }

  /* dropdown menu (baseweb) */
  div[role="listbox"]{
    background-color: var(--gl-panel-2) !important;
    border: 1px solid var(--gl-border) !important;
    color: var(--gl-text) !important;
  }
  div[role="option"]{
    color: var(--gl-text) !important;
  }
  div[role="option"][aria-selected="true"]{
    background-color: rgba(0,255,102,0.14) !important;
  }
  div[role="option"]:hover{
    background-color: rgba(0,255,102,0.10) !important;
  }

  /* slider */
  section[data-testid="stSidebar"] div[data-baseweb="slider"] *,
  div[data-testid="stSidebar"] div[data-baseweb="slider"] *{
    color: var(--gl-text) !important;
  }
  section[data-testid="stSidebar"] div[data-baseweb="slider"] div[role="slider"],
  div[data-testid="stSidebar"] div[data-baseweb="slider"] div[role="slider"]{
    background-color: var(--gl-accent) !important;
    border: 1px solid rgba(231,255,231,0.6) !important;
  }
  section[data-testid="stSidebar"] div[data-baseweb="slider"] div[aria-valuemin],
  div[data-testid="stSidebar"] div[data-baseweb="slider"] div[aria-valuemin]{
    background-color: rgba(0,255,102,0.20) !important;
  }

  /* checkbox */
  section[data-testid="stSidebar"] div[role="checkbox"],
  div[data-testid="stSidebar"] div[role="checkbox"]{
    border-radius: 6px !important;
  }

  /* button in sidebar */
  section[data-testid="stSidebar"] .stButton > button,
  div[data-testid="stSidebar"] .stButton > button{
    width: 100%;
    background: linear-gradient(180deg, rgba(0,255,102,0.18), rgba(0,255,102,0.10)) !important;
    border: 1px solid rgba(0,255,102,0.55) !important;
    color: var(--gl-text) !important;
  }
  section[data-testid="stSidebar"] .stButton > button:hover,
  div[data-testid="stSidebar"] .stButton > button:hover{
    background: linear-gradient(180deg, rgba(0,255,102,0.28), rgba(0,255,102,0.14)) !important;
    border-color: rgba(0,255,102,0.90) !important;
    color: var(--gl-text) !important;
  }
  section[data-testid="stSidebar"] button[kind="primary"],
  div[data-testid="stSidebar"] button[kind="primary"]{
    background: linear-gradient(180deg, rgba(0,255,102,0.28), rgba(0,255,102,0.14)) !important;
    border: 1px solid rgba(0,255,102,0.95) !important;
    color: var(--gl-text) !important;
  }
  section[data-testid="stSidebar"] button[kind="primary"]:hover,
  div[data-testid="stSidebar"] button[kind="primary"]:hover{
    background: linear-gradient(180deg, rgba(0,255,102,0.40), rgba(0,255,102,0.20)) !important;
    border-color: rgba(0,255,102,1.0) !important;
  }

  /* Header */
  .gl-header{ display:flex; align-items:center; gap:14px; padding: 10px 12px; border:1px solid var(--gl-border); border-radius: 12px; background: linear-gradient(180deg, rgba(0,255,102,0.06), rgba(0,0,0,0)); }
  .gl-logo{ width:34px; height:34px; flex:0 0 auto; }
  .gl-title{ display:flex; flex-direction:column; line-height:1.1; }
  .gl-title .gl-h1{ font-size: 1.6rem; font-weight: 700; letter-spacing: 0.2px; }
  .gl-title .gl-sub{ color: var(--gl-muted); font-size: 0.95rem; margin-top: 2px; }

  /* Metric cards */
  .stMetric{
    background: linear-gradient(180deg, rgba(0,255,102,0.06) 0%, rgba(10,18,14,1) 55%);
    border: 1px solid var(--gl-border);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    box-shadow: none;
  }
  .stMetric [data-testid="stMetricValue"]{ color: var(--gl-accent); }
  .stMetric [data-testid="stMetricLabel"]{ color: var(--gl-text); }

  /* Buttons */
  .stButton > button,
  .stDownloadButton > button,
  div[data-baseweb="button"] > button{
    border-radius: 10px !important;
    font-weight: 650 !important;
    background-color: var(--gl-panel) !important;
    color: var(--gl-text) !important;
    border: 1px solid rgba(0,255,102,0.45) !important;
    box-shadow: none !important;
    transition: transform 0.12s ease, box-shadow 0.12s ease, background-color 0.12s ease, border-color 0.12s ease, color 0.12s ease !important;
  }
  .stButton > button:hover,
  .stDownloadButton > button:hover,
  div[data-baseweb="button"] > button:hover{
    transform: translateY(-1px);
    background-color: rgba(0,255,102,0.12) !important;
    border-color: rgba(0,255,102,0.90) !important;
    color: var(--gl-text) !important;
    box-shadow: 0 10px 24px rgba(0,0,0,0.45) !important;
  }
  .stButton > button:active,
  .stDownloadButton > button:active,
  div[data-baseweb="button"] > button:active{
    transform: translateY(0px);
    background-color: rgba(0,255,102,0.20) !important;
  }
  .stButton > button:focus,
  .stDownloadButton > button:focus,
  div[data-baseweb="button"] > button:focus{
    outline: 2px solid rgba(0,255,102,0.55) !important;
    outline-offset: 2px !important;
  }

  button[kind="primary"]{
    background: linear-gradient(180deg, rgba(0,255,102,0.26), rgba(0,255,102,0.14)) !important;
    border: 1px solid rgba(0,255,102,0.85) !important;
    color: var(--gl-text) !important;
  }
  button[kind="primary"]:hover{
    background: linear-gradient(180deg, rgba(0,255,102,0.40), rgba(0,255,102,0.22)) !important;
    border-color: rgba(0,255,102,1.0) !important;
  }

  /* Dataframe */
  div[data-testid="stDataFrame"]{
    border: 1px solid var(--gl-border);
    border-radius: 12px;
    overflow: hidden;
  }
</style>
""",
    unsafe_allow_html=True,
)

# Header (SVG, no emoji)
_LOGO_SVG = """
<svg class="gl-logo" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GammaLab">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#00ff66" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#00cc55" stop-opacity="0.9"/>
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="29" fill="none" stroke="url(#g)" stroke-width="3"/>
  <path d="M38 14c-8 0-14 6-14 14v22h7V28c0-4 3-7 7-7h2v-7h-2z" fill="url(#g)"/>
</svg>
"""
st.markdown(
    f"""
<div class="gl-header">
  {_LOGO_SVG}
  <div class="gl-title">
    <div class="gl-h1">GammaLab</div>
    <div class="gl-sub">Simulatore di attenuazione dei raggi gamma</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Mappatura materiali (etichette UI → chiavi modello)
MATERIAL_MAP = {
    "Piombo": "Pb",
    "Alluminio": "Al",
    "Acqua": "H2O",
    "Aria": "Air",
    "Tessuto": "Tissue",
}


@st.cache_data(show_spinner=False)
def cached_transmission(material_key: str, energy_mev: float, thickness_cm: float) -> float:
    """Cached transmission helper."""
    return models.transmission_fraction(material_key, energy_mev, thickness_cm)


@st.cache_data(show_spinner=False)
def cached_interaction_probabilities(material_key: str, energy_mev: float) -> dict:
    """Cached interaction-probability helper."""
    return models.interaction_probabilities(material_key, energy_mev)


@st.cache_data(show_spinner=False)
def cached_material_table(energy_mev: float, thickness_mm: float) -> pd.DataFrame:
    """Tabella confronto materiali (cache)."""
    thickness_cm = thickness_mm / 10.0
    rows = []
    for mat_name, mat_key in MATERIAL_MAP.items():
        mu_val = models.mu_cm_inv(mat_key, energy_mev)
        hvl_cm_val = models.half_value_layer_cm(mat_key, energy_mev)
        rows.append(
            {
                "Materiale": mat_name,
                "Z_eff": f"{models.get_materials()[mat_key].z_eff:.1f}",
                "μ (cm⁻¹)": f"{mu_val:.4f}",
                "HVL (mm)": f"{hvl_cm_val * 10.0:.2f}",
                "HVL (cm)": f"{hvl_cm_val:.4f}",
                f"Trasmissione a {thickness_mm:.1f} mm": f"{models.transmission_fraction(mat_key, energy_mev, thickness_cm):.4f}",
            }
        )
    return pd.DataFrame(rows)


def _run_monte_carlo(
    material_key: str,
    energy_mev: float,
    thickness_cm: float,
    n_photons: int,
    seed: int | None,
) -> dict:
    """Esegue la simulazione Monte Carlo (senza cache per seed=None, così ogni run è diversa)."""
    return sim.run_monte_carlo(
        material_key=material_key,
        energy_mev=energy_mev,
        thickness_cm=thickness_cm,
        n_photons=n_photons,
        seed=seed,
    )

# Controlli sidebar
st.sidebar.header("Controlli simulazione")

# Slider energia
energy = st.sidebar.slider(
    "Energia fotone (MeV)",
    min_value=0.05,
    max_value=10.0,
    value=1.0,
    step=0.01,
    help="Energia del fotone gamma incidente",
)

# Indicatore soglia produzione di coppie
st.sidebar.markdown("---")
if energy < 1.022:
    st.sidebar.warning(f"""
    **Soglia produzione di coppie: 1,022 MeV**

    Energia attuale: **{energy:.3f} MeV**

    Sotto soglia: produzione di coppie **non possibile**.

    La produzione di coppie richiede energia ≥ 1,022 MeV (2 × massa a riposo dell’elettrone).
    """)
else:
    st.sidebar.success(f"""
    **Produzione di coppie: ATTIVA**

    Energia: **{energy:.3f} MeV** > soglia 1,022 MeV.

    La produzione di coppie può avvenire a questa energia.
    """)
st.sidebar.markdown("---")

# Materiale
material_name = st.sidebar.selectbox(
    "Materiale",
    options=list(MATERIAL_MAP.keys()),
    help="Materiale attraversato dal fotone",
)
material_key = MATERIAL_MAP[material_name]

# Spessore (mm)
st.sidebar.markdown("### Spessore")
thickness_mm = st.sidebar.slider(
    "Spessore (mm)",
    min_value=0.0,
    max_value=50.0,
    value=5.0,
    step=0.1,
    help="Spessore del materiale in millimetri",
)

# Spessore massimo per il grafico
max_thickness_mm = st.sidebar.slider(
    "Intervallo grafico (spessore max, mm)",
    min_value=1.0,
    max_value=100.0,
    value=50.0,
    step=1.0,
    help="Spessore massimo mostrato nel grafico di attenuazione",
)

# Controlli Monte Carlo
st.sidebar.markdown("---")
st.sidebar.markdown("### Simulazione Monte Carlo")

n_photons = st.sidebar.number_input(
    "Numero di fotoni (N)",
    min_value=1000,
    max_value=100000,
    value=10000,
    step=1000,
    help="Numero di fotoni da simulare (più alto = più preciso ma più lento)",
)

if n_photons > 50000:
    st.sidebar.warning("N elevato può essere lento. Per uso interattivo conviene 10.000–50.000.")
elif n_photons > 20000:
    st.sidebar.info("N elevato può richiedere alcuni secondi.")

use_seed = st.sidebar.checkbox("Usa seed casuale (per riproducibilità)", value=False)
seed = None
if use_seed:
    seed = st.sidebar.number_input(
        "Seed casuale",
        min_value=0,
        max_value=2147483647,
        value=42,
        help="Seed per risultati riproducibili",
    )
else:
    st.sidebar.caption("Senza seed ogni esecuzione dà risultati diversi.")

# Pulsante avvio
run_simulation = st.sidebar.button("Esegui simulazione Monte Carlo", type="primary")

# Convert thickness to cm for calculations
thickness_cm = thickness_mm / 10.0

# Validazione input
if thickness_cm == 0:
    st.info("**Spessore zero:** senza materiale tutti i fotoni vengono trasmessi (I/I₀ = 1,0).")
elif thickness_cm < 0:
    st.error("**Spessore non valido:** non può essere negativo.")
    st.stop()

if energy <= 0.05:
    st.warning("**Energia molto bassa:** a energie molto basse domina l’effetto fotoelettrico, soprattutto per materiali ad alto Z.")
elif energy >= 10.0:
    st.info("**Energia alta:** a energie alte la produzione di coppie diventa significativa, soprattutto per materiali ad alto Z.")

# Main content area
st.markdown("---")

# Trasmissione attuale
try:
    current_transmission = cached_transmission(material_key, energy, thickness_cm)
except (ValueError, KeyError) as e:
    st.error(f"**Errore di calcolo:** {str(e)}")
    st.stop()

# Calculate interaction probabilities
interaction_probs = cached_interaction_probabilities(material_key, energy)

# Riga metriche
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Energia fotone", f"{energy:.3f} MeV")
    st.caption("Energia del fotone gamma incidente")
with col2:
    st.metric("Materiale", material_name)
    st.caption(f"Z_eff ≈ {models.get_materials()[material_key].z_eff:.1f}")
with col3:
    st.metric("Trasmissione I/I₀", f"{current_transmission:.4f}")
    st.caption("Frazione di fotoni che attraversano il materiale")

st.markdown(f"**Spessore attuale:** {thickness_mm:.2f} mm ({thickness_cm:.2f} cm)")
if thickness_cm == 0:
    st.info("Senza materiale il 100% dei fotoni viene trasmesso.")
elif thickness_cm < 0.1:
    st.info("Materiale molto sottile: la maggior parte dei fotoni verrà probabilmente trasmessa.")
elif thickness_cm > 10:
    st.info("Materiale spesso: attenuazione significativa, soprattutto a basse energie.")

st.markdown("---")

tab_grafici, tab_dati, tab_monte_carlo = st.tabs(["Grafici", "Dati", "Monte Carlo"])

fig_attenuation = None
fig_interactions = None

with tab_grafici:
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Curva di attenuazione")
        st.caption(
            "La trasmissione (I/I₀) diminuisce in modo esponenziale con lo spessore. Il marcatore indica lo spessore selezionato. Legge di Beer-Lambert: I(x) = I₀ × exp(-μx)."
        )
        try:
            fig_attenuation = plot_transmission_vs_thickness(
                material_key=material_key,
                energy_mev=energy,
                max_thickness_mm=max_thickness_mm,
                current_thickness_mm=thickness_mm,
                transmission_func=cached_transmission,
            )
            st.plotly_chart(fig_attenuation, use_container_width=True)
        except Exception as e:
            st.error(f"Errore grafico: impossibile generare il grafico di attenuazione. {str(e)}")
            st.info("Prova a modificare energia o materiale.")

        if fig_attenuation is not None:
            col_export1, col_export2 = st.columns(2)
            with col_export1:
                try:
                    png_data = export.figure_to_png(fig_attenuation)
                    st.download_button(
                        label="Scarica PNG",
                        data=png_data,
                        file_name=f"attenuation_{material_key}_{energy:.2f}MeV.png",
                        mime="image/png",
                        key="download_attenuation_png",
                    )
                except ImportError:
                    st.caption("Per esportare PNG: `pip install kaleido`")
            with col_export2:
                try:
                    pdf_data = export.figure_to_pdf(fig_attenuation)
                    st.download_button(
                        label="Scarica PDF",
                        data=pdf_data,
                        file_name=f"attenuation_{material_key}_{energy:.2f}MeV.pdf",
                        mime="application/pdf",
                        key="download_attenuation_pdf",
                    )
                except ImportError:
                    st.caption("Per esportare PDF: `pip install kaleido`")

    with col_right:
        st.subheader("Probabilità di interazione")
        st.caption("Probabilità relative di ogni tipo di interazione quando un fotone interagisce.")
        try:
            fig_interactions = plot_interaction_probabilities(interaction_probs, energy)
            st.plotly_chart(fig_interactions, use_container_width=True)
        except Exception as e:
            st.error(f"Errore grafico: impossibile generare il grafico delle interazioni. {str(e)}")

        if fig_interactions is not None:
            col_export3, col_export4 = st.columns(2)
            with col_export3:
                try:
                    png_data = export.figure_to_png(fig_interactions)
                    st.download_button(
                        label="Scarica PNG",
                        data=png_data,
                        file_name=f"interactions_{material_key}_{energy:.2f}MeV.png",
                        mime="image/png",
                        key="download_interactions_png",
                    )
                except ImportError:
                    st.caption("Richiede kaleido")
            with col_export4:
                try:
                    pdf_data = export.figure_to_pdf(fig_interactions)
                    st.download_button(
                        label="Scarica PDF",
                        data=pdf_data,
                        file_name=f"interactions_{material_key}_{energy:.2f}MeV.pdf",
                        mime="application/pdf",
                        key="download_interactions_pdf",
                    )
                except ImportError:
                    st.caption("Richiede kaleido")

        st.markdown("### Meccanismi di interazione")
        if interaction_probs["photoelectric"] > 0.5:
            st.info("L’effetto fotoelettrico domina a basse energie, soprattutto per materiali ad alto Z.")
        elif interaction_probs["compton"] > 0.5:
            st.info("Lo scattering Compton domina a energie intermedie (~0,2–5 MeV).")
        elif interaction_probs["pair"] > 0.5:
            st.info("La produzione di coppie domina ad alte energie (>1,022 MeV), soprattutto per materiali ad alto Z.")
        else:
            st.info("Più meccanismi contribuiscono in modo significativo.")

        if energy < 1.022:
            st.warning("Produzione di coppie non possibile sotto 1,022 MeV.")
        else:
            st.success("Produzione di coppie possibile a questa energia.")

    st.markdown("---")
    st.subheader("Sweep in energia (spessore fissato)")
    st.caption("Come varia la trasmissione con l’energia per il materiale e lo spessore attuali.")
    try:
        fig_energy_sweep = plot_transmission_vs_energy(
            material_key=material_key,
            thickness_mm=thickness_mm,
            transmission_func=cached_transmission,
        )
        st.plotly_chart(fig_energy_sweep, use_container_width=True)
        sweep_col1, sweep_col2 = st.columns(2)
        with sweep_col1:
            try:
                sweep_png = export.figure_to_png(fig_energy_sweep)
                st.download_button(
                    label="Scarica PNG sweep energia",
                    data=sweep_png,
                    file_name=f"energy_sweep_{material_key}_{thickness_mm:.1f}mm.png",
                    mime="image/png",
                    key="download_energy_sweep_png",
                )
            except ImportError:
                st.caption("Richiede kaleido.")
        with sweep_col2:
            try:
                sweep_pdf = export.figure_to_pdf(fig_energy_sweep)
                st.download_button(
                    label="Scarica PDF sweep energia",
                    data=sweep_pdf,
                    file_name=f"energy_sweep_{material_key}_{thickness_mm:.1f}mm.pdf",
                    mime="application/pdf",
                    key="download_energy_sweep_pdf",
                )
            except ImportError:
                st.caption("Richiede kaleido.")
    except Exception as error:
        st.error(f"Impossibile generare il grafico sweep energia: {error}")

with tab_dati:
    st.subheader("Dati e parametri")
    st.caption("Riepilogo numerico, coefficienti e confronto materiali.")

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown("### Parametri attuali")
        st.write(f"- **Energia:** {energy:.3f} MeV")
        st.write(f"- **Materiale:** {material_name} (Z_eff ≈ {models.get_materials()[material_key].z_eff:.1f})")
        st.write(f"- **Spessore:** {thickness_mm:.2f} mm = {thickness_cm:.2f} cm")
        st.write(f"- **Trasmissione:** I/I₀ = {current_transmission:.6f}")
        st.write(f"- **Coefficiente di attenuazione (μ):** {models.mu_cm_inv(material_key, energy):.4f} cm⁻¹")
        hvl_cm = models.half_value_layer_cm(material_key, energy)
        hvl_mm = hvl_cm * 10.0
        st.write(f"- **Strato semiassorbente (HVL):** {hvl_mm:.2f} mm = {hvl_cm:.4f} cm")

    with col_info2:
        st.markdown("### Probabilità di interazione")
        st.write(f"- **Fotoelettrico:** {interaction_probs['photoelectric']:.1%}")
        st.write(f"- **Compton:** {interaction_probs['compton']:.1%}")
        st.write(f"- **Produzione di coppie:** {interaction_probs['pair']:.1%}")
        total = sum(interaction_probs.values())
        st.caption(f"Totale: {total:.6f}")

    st.markdown("---")
    st.subheader("Confronto materiali")
    st.caption("Confronto alle impostazioni di energia e spessore attuali. HVL = spessore per cui I/I₀ = 0,5.")

    df_comparison = cached_material_table(energy, thickness_mm)
    try:
        styler = (
            df_comparison.style.set_table_styles(
                [
                    {"selector": "th", "props": "background-color:#07100c;color:#00ff66;border:1px solid #123321;"},
                    {"selector": "td", "props": "border:1px solid #123321;color:#e7ffe7;background-color:#0a120e;"},
                ]
            )
            .set_properties(**{"font-size": "0.95rem"})
        )
        st.dataframe(styler, use_container_width=True, hide_index=True)
    except Exception:
        # Fallback se lo styling non è supportato in qualche ambiente
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)

with tab_monte_carlo:
    st.subheader("Simulazione Monte Carlo")
    st.caption("Campionamento statistico di trasmissione e interazioni (senza seed: run diverse; con seed: riproducibile).")

    st.markdown(
        """
**Funzionamento:**
1. Per ogni fotone si decide se interagisce nello spessore con probabilità = 1 - exp(-μx).
2. In caso di interazione, il tipo viene scelto casualmente in base alle probabilità.
3. Si contano fotoni trasmessi e interazioni per tipo.
"""
    )

    if run_simulation:
        with st.spinner(f"Simulazione in corso ({n_photons:,} fotoni)..."):
            try:
                mc_results = _run_monte_carlo(
                    material_key=material_key,
                    energy_mev=energy,
                    thickness_cm=thickness_cm,
                    n_photons=n_photons,
                    seed=seed,
                )
            except (ValueError, KeyError) as error:
                st.error(f"Errore Monte Carlo: {error}")
                mc_results = None

        if mc_results is not None:
            st.session_state["mc_results"] = mc_results
            st.session_state["mc_ran"] = True

# Display results if simulation has been run
if 'mc_ran' in st.session_state and st.session_state['mc_ran']:
    mc_results = st.session_state['mc_results']
    fig_pie = None
    fig_bar = None
    
    col_mc1, col_mc2, col_mc3, col_mc4 = st.columns(4)
    with col_mc1:
        st.metric("Trasmessi", f"{mc_results['transmitted']:,}", delta=f"{mc_results['transmitted_fraction']:.2%}")
    with col_mc2:
        st.metric("Interazioni", f"{mc_results['interactions']:,}", delta=f"{mc_results['interaction_fraction']:.2%}")
    with col_mc3:
        analytical = mc_results['analytical_transmission']
        simulated = mc_results['transmitted_fraction']
        diff = simulated - analytical
        st.metric("I/I₀ analitico", f"{analytical:.4f}", delta=f"Δ = {diff:+.4f}", delta_color="normal")
    with col_mc4:
        st.metric("I/I₀ simulato", f"{simulated:.4f}", delta=f"Errore: {abs(diff):.4f}")

    error_pct = abs(diff) / analytical * 100 if analytical > 0 else 0
    if error_pct < 1.0:
        st.success(f"La simulazione coincide con il risultato analitico entro {error_pct:.2f}%")
    elif error_pct < 5.0:
        st.info(f"Simulazione entro {error_pct:.2f}% dal risultato analitico (campionamento statistico)")
    else:
        st.warning(f"La simulazione si discosta del {error_pct:.2f}% dal risultato analitico. Prova ad aumentare N.")
    
    # Plots
    col_mc_plot1, col_mc_plot2 = st.columns(2)
    
    with col_mc_plot1:
        st.markdown("### Esiti della simulazione")
        fig_pie = plot_monte_carlo_results(mc_results)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Export buttons for pie chart
        col_mc_export1, col_mc_export2 = st.columns(2)
        with col_mc_export1:
            try:
                png_data = export.figure_to_png(fig_pie)
                st.download_button(
                    label="Scarica PNG",
                    data=png_data,
                    file_name=f"monte_carlo_pie_{material_key}_{energy:.2f}MeV.png",
                    mime="image/png",
                    key="download_mc_pie_png"
                )
            except ImportError:
                st.caption("Richiede kaleido")
        with col_mc_export2:
            try:
                pdf_data = export.figure_to_pdf(fig_pie)
                st.download_button(
                    label="Scarica PDF",
                    data=pdf_data,
                    file_name=f"monte_carlo_pie_{material_key}_{energy:.2f}MeV.pdf",
                    mime="application/pdf",
                    key="download_mc_pie_pdf"
                )
            except ImportError:
                st.caption("Richiede kaleido")
    
    with col_mc_plot2:
        st.markdown("### Ripartizione per tipo di interazione")
        fig_bar = plot_monte_carlo_interactions(mc_results)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Export buttons for bar chart
        col_mc_export3, col_mc_export4 = st.columns(2)
        with col_mc_export3:
            try:
                png_data = export.figure_to_png(fig_bar)
                st.download_button(
                    label="Scarica PNG",
                    data=png_data,
                    file_name=f"monte_carlo_bar_{material_key}_{energy:.2f}MeV.png",
                    mime="image/png",
                    key="download_mc_bar_png"
                )
            except ImportError:
                st.caption("Richiede kaleido")
        with col_mc_export4:
            try:
                pdf_data = export.figure_to_pdf(fig_bar)
                st.download_button(
                    label="Scarica PDF",
                    data=pdf_data,
                    file_name=f"monte_carlo_bar_{material_key}_{energy:.2f}MeV.pdf",
                    mime="application/pdf",
                    key="download_mc_bar_pdf"
                )
            except ImportError:
                st.caption("Richiede kaleido")

    if fig_attenuation is not None and fig_interactions is not None:
        st.markdown("### Esporta report")
        try:
            report_pdf = export.create_report_pdf(
                fig_attenuation=fig_attenuation,
                fig_interactions=fig_interactions,
                fig_monte_carlo=fig_pie,
                title=f"GammaLab Report - {material_name} - {energy:.2f} MeV",
            )
            st.download_button(
                label="Scarica report PDF (singola pagina)",
                data=report_pdf,
                file_name=f"gammalab_report_{material_key}_{energy:.2f}MeV.pdf",
                mime="application/pdf",
                key="download_report_pdf",
            )
        except ImportError:
            st.caption("Il report PDF richiede `reportlab` e `kaleido`.")
    
    st.markdown("### Dettaglio risultati")
    col_detail1, col_detail2 = st.columns(2)
    with col_detail1:
        st.markdown("#### Trasmissione")
        st.write(f"- **Fotoni trasmessi:** {mc_results['transmitted']:,} ({mc_results['transmitted_fraction']:.2%})")
        st.write(f"- **Fotoni che hanno interagito:** {mc_results['interactions']:,} ({mc_results['interaction_fraction']:.2%})")
        st.write(f"- **Trasmissione analitica:** {mc_results['analytical_transmission']:.6f}")
        st.write(f"- **Trasmissione simulata:** {mc_results['transmitted_fraction']:.6f}")
    with col_detail2:
        st.markdown("#### Interazioni per tipo")
        if mc_results['interactions'] > 0:
            st.write(f"- **Fotoelettrico:** {mc_results['photoelectric_count']:,} ({mc_results['photoelectric_fraction']:.2%})")
            st.write(f"- **Compton:** {mc_results['compton_count']:,} ({mc_results['compton_fraction']:.2%})")
            st.write(f"- **Produzione di coppie:** {mc_results['pair_count']:,} ({mc_results['pair_fraction']:.2%})")
        else:
            st.write("Nessuna interazione (tutti i fotoni trasmessi).")
    
    st.info("Nota: i risultati Monte Carlo hanno fluttuazioni statistiche; aumentando N la stima converge.")
else:
    st.info("Esegui la simulazione dalla barra laterale per vedere i risultati.")

# Disclaimer e note solo alla fine
st.markdown("---")
st.subheader("Avvertenze e limitazioni")

st.markdown(
    """
<div style='background-color: #0a120e; padding: 16px; border: 1px solid #123321; border-left: 4px solid #00ff66; border-radius: 10px; margin: 12px 0;'>
  <h4 style='margin:0 0 8px 0; color:#00ff66;'>Solo uso didattico</h4>
  <p style='margin:0; color:#e7ffe7;'>
    GammaLab utilizza modelli semplificati ed euristici. Non usare per applicazioni mediche, ingegneristiche o di sicurezza.
    Per calcoli precisi usare banche dati NIST, software validati e consultare professionisti qualificati.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("Dettagli (cosa mostra e cosa non mostra)"):
    st.markdown(
        """
**Cosa mostra:**
- Modelli semplificati di attenuazione (Beer-Lambert) e confronto materiali
- Probabilità di interazione euristiche (fotoelettrico, Compton, produzione di coppie)
- Esempio Monte Carlo per osservare la variabilità statistica

**Cosa non mostra:**
- Sezioni d’urto reali e dipendenze dettagliate da energia/composizione
- Deposizione di energia, dose, geometrie complesse, secondari, effetti avanzati
"""
    )

st.caption("GammaLab – Simulatore didattico di attenuazione dei raggi gamma | Versione 1.0")

