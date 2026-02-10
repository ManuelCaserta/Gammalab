# GammaLab

A didactic simulator of gamma-ray attenuation and interaction mechanisms (photoelectric, Compton, pair production).

## Setup

1. **Install Python 3.11+** (if not already installed)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Launch the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Run Tests

```bash
pytest tests -v
```

Some test modules skip automatically if optional plotting/report dependencies are unavailable.

## Tutorial

See `TUTORIAL.md` for a classroom-oriented walkthrough.

## Project Structure

```
GammaLab/
├── app.py                 # Streamlit entrypoint
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── TUTORIAL.md            # Step-by-step user guide
├── gammalab/             # Main package
│   ├── __init__.py
│   ├── materials.json     # Material configuration
│   ├── models.py          # Physics/math functions
│   ├── sim.py             # Monte Carlo simulation
│   ├── ui.py              # UI helper/plot functions
│   └── export.py          # PNG/PDF export helpers
└── tests/                # Unit tests
    ├── test_models.py
    ├── test_sim.py
    ├── test_ui.py
    └── test_export.py
```

## Development

This is a school project designed to be beginner-readable while maintaining clean code structure. The physics logic will be implemented in subsequent development phases.

