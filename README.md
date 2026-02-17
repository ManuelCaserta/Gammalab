# GammaLab

Simulatore didattico di attenuazione dei raggi gamma e dei meccanismi di interazione (effetto fotoelettrico, Compton, produzione di coppie).

## Installazione

1. **Installa Python 3.11 o superiore** (se non è già installato).

2. **Crea un ambiente virtuale** (consigliato):
   ```bash
   python -m venv venv
   ```

3. **Attiva l’ambiente virtuale**:
   - Su Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Su macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

## Avvio dell’app

Per avviare l’applicazione Streamlit:
```bash
streamlit run app.py
```

L’app si aprirà nel browser predefinito all’indirizzo `http://localhost:8501`.

## Eseguire i test

```bash
pytest tests -v
```

Alcuni test vengono saltati automaticamente se le dipendenze opzionali (grafici/report) non sono disponibili.

## Tutorial

Consulta `TUTORIAL.md` per una guida passo-passo pensata per l’uso in aula.

## Struttura del progetto

```
GammaLab/
├── app.py                 # Punto di ingresso Streamlit
├── requirements.txt       # Dipendenze Python
├── README.md              # Questo file
├── TUTORIAL.md            # Guida utente passo-passo
├── assets/                # Icone (es. SVG)
├── gammalab/              # Pacchetto principale
│   ├── __init__.py
│   ├── materials.json     # Configurazione materiali
│   ├── models.py          # Funzioni fisica/matematica
│   ├── sim.py             # Simulazione Monte Carlo
│   ├── ui.py              # Grafici e helper interfaccia
│   └── export.py          # Esportazione PNG/PDF
└── tests/                 # Test unitari
    ├── test_models.py
    ├── test_sim.py
    ├── test_ui.py
    └── test_export.py
```

## Sviluppo

Progetto didattico pensato per essere leggibile anche da chi è alle prime armi, mantenendo una struttura di codice ordinata. La logica fisica può essere estesa nelle fasi successive di sviluppo.
