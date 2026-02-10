# GammaLab Quick Tutorial

This tutorial is for classroom/lab learning.

## 1) Start the app

```bash
streamlit run app.py
```

## 2) Set base parameters

In the sidebar:
- Choose **Photon Energy (MeV)**
- Choose **Material**
- Choose **Thickness (mm)**

The app converts thickness to cm internally.

## 3) Read the main outputs

- **Transmission I/I0**: fraction that passes through material.
- **Attenuation Curve**: how transmission changes with thickness.
- **Interaction Probabilities**: relative chance of interaction type.

Important: Pair production appears only above **1.022 MeV**.

## 4) Compare materials

In the material table, compare:
- `μ (cm⁻¹)` attenuation coefficient
- `HVL` half-value layer
- transmission at current thickness

Lower HVL generally means stronger shielding.

## 5) Run Monte Carlo

- Set number of photons (default 10,000)
- Optional: set a seed for reproducibility
- Click **Run Monte Carlo Simulation**

Compare simulated transmission with analytical transmission.

## 6) Export plots and report

Use download buttons under plots:
- PNG
- PDF

You can also export a single-page PDF report.

## Notes

- GammaLab uses simplified educational models.
- It is **not** a clinical/engineering safety tool.

