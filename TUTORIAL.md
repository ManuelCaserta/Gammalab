# Tutorial GammaLab

Questo tutorial spiega come usare GammaLab passo per passo. È pensato per lezioni e laboratori: ogni sezione dice **cosa fare**, **dove farlo** e **perché**.

---

## 1. Avviare l’applicazione

**Cosa fare:** apri un terminale nella cartella del progetto e lancia:

```bash
streamlit run app.py
```

**Cosa succede:** si apre una pagina nel browser (di solito `http://localhost:8501`). Vedrai la schermata principale con titolo “GammaLab” e una barra laterale a sinistra con i controlli.

**Se non parte:** controlla di aver attivato l’ambiente virtuale e di aver installato le dipendenze (`pip install -r requirements.txt`).

---

## 2. Capire la barra laterale (controlli)

Tutti i parametri della simulazione si cambiano **nella barra laterale a sinistra**.

### 2.1 Energia del fotone (MeV)

- **Cosa è:** l’energia del raggio gamma che “colpisce” il materiale, in megaelettronvolt (MeV).
- **Cosa fare:** sposta lo slider o inserisci un valore (es. 1,0 MeV).
- **Perché è importante:** a energie basse domina l’effetto fotoelettrico; sopra 1,022 MeV entra in gioco anche la produzione di coppie. L’app ti avvisa se sei sotto o sopra questa soglia.

### 2.2 Materiale

- **Cosa è:** il materiale attraverso cui passano i fotoni (es. Piombo, Acqua, Tessuto).
- **Cosa fare:** scegli dal menu a tendina (Piombo, Alluminio, Acqua, Aria, Tessuto).
- **Perché è importante:** materiali diversi attenuano in modo diverso (il piombo attenua molto, l’aria poco). Lo vedrai nei grafici e nella tabella confronto.

### 2.3 Spessore (mm)

- **Cosa è:** lo spessore del materiale in millimetri (l’app converte in cm per i calcoli).
- **Cosa fare:** imposta lo spessore con lo slider (es. 5 mm).
- **Perché è importante:** più è spesso il materiale, meno fotoni passano. La “Curva di attenuazione” mostra proprio come la trasmissione scende all’aumentare dello spessore.

### 2.4 Intervallo grafico (spessore max)

- **Cosa è:** lo spessore massimo mostrato nel grafico “Trasmissione vs spessore”.
- **Cosa fare:** lascia il valore di default (es. 50 mm) o aumentalo se vuoi vedere la curva fino a spessori maggiori.

---

## 3. Leggere i risultati principali

Sopra e sotto i grafici trovi numeri e spiegazioni. Ecco cosa significano.

### 3.1 Le tre “metriche” in alto

- **Energia fotone:** il valore che hai scelto (es. 1,000 MeV).
- **Materiale:** il materiale selezionato e il suo Z efficace (indicatore di “peso” del materiale).
- **Trasmissione I/I₀:** la **frazione di fotoni che attraversa** il materiale allo spessore scelto.  
  Esempio: 0,85 significa che l’85% dei fotoni passa, il 15% viene assorbito o deviato.

### 3.2 Curva di attenuazione

- **Cosa mostra:** un grafico dove sull’asse orizzontale c’è lo **spessore** (mm) e sull’asse verticale la **trasmissione** (da 0 a 1).
- **Come leggerlo:** la curva scende man mano che lo spessore aumenta (legge di Beer-Lambert). Il **puntino verde** indica il valore corrispondente allo spessore che hai scelto nella sidebar.

### 3.3 Probabilità di interazione

- **Cosa mostra:** tre barre (Fotoelettrico, Compton, Produzione di coppie) che indicano **quanto è probabile** ciascun tipo di interazione quando un fotone interagisce.
- **Nota importante:** la produzione di coppie è possibile **solo sopra 1,022 MeV**. Sotto questa energia la barra “Produzione di coppie” è zero e l’app lo segnala.

---

## 4. Tab “Dati” e confronto materiali

Nella tab **Dati** trovi:

- **Parametri attuali:** energia, materiale, spessore, trasmissione, coefficiente di attenuazione μ, strato semiassorbente (HVL).
- **Probabilità di interazione:** percentuali fotoelettrico, Compton, produzione di coppie.
- **Tabella confronto materiali:** tutti i materiali messi a confronto alle stesse energia e spessore.

**Cosa guardare nella tabella:**

- **μ (cm⁻¹):** coefficiente di attenuazione. Valori più alti = attenuazione più forte.
- **HVL (mm o cm):** spessore per cui la trasmissione è 0,5 (metà dei fotoni passa). **HVL più basso = migliore schermatura** (es. piombo). In radioterapia spesso interessano materiali con HVL più alto.
- **Trasmissione a X mm:** la frazione di fotoni che passa per quel materiale allo spessore indicato.

---

## 5. Simulazione Monte Carlo

La simulazione Monte Carlo **simula** il destino di molti fotoni uno per uno (casuale) e ti fa vedere se i numeri “a caso” si avvicinano alla formula teorica (Beer-Lambert).

### 5.1 Dove si trova

Nella barra laterale, sotto Spessore, c’è la sezione **“Simulazione Monte Carlo”**.

### 5.2 Cosa impostare

- **Numero di fotoni (N):** quanti fotoni simulare (es. 10.000). Più è alto N, più il risultato è vicino al valore analitico, ma il calcolo è più lento.
- **Usa seed casuale:** se **non** lo attivi, ogni volta che clicchi “Esegui” ottieni un risultato leggermente diverso (è normale). Se lo attivi e inserisci un numero (es. 42), i risultati diventano **riproducibili**: stesso seed → stesso risultato.

### 5.3 Cosa fare

Clicca **“Esegui simulazione Monte Carlo”**. Dopo qualche secondo compaiono:

- **Metriche:** fotoni trasmessi, interazioni, confronto tra trasmissione analitica e simulata.
- **Grafici:** torta (esiti: trasmessi vs tipi di interazione) e barre (conteggi per tipo di interazione).

**Come interpretare:** se la “Trasmissione simulata” è vicina alla “Trasmissione analitica”, la simulazione sta funzionando bene. Piccole differenze sono normali (errore statistico); aumentando N si riducono.

---

## 6. Esportare grafici e report

Sotto molti grafici trovi pulsanti per scaricare:

- **Scarica PNG** / **Scarica PDF:** salva il singolo grafico in PNG o PDF.
- Nella sezione Monte Carlo, dopo aver eseguito una simulazione, puoi anche **Scarica report PDF (singola pagina)** per un riepilogo con più figure.

**Nota:** per l’esportazione PDF/PNG dei grafici serve la libreria `kaleido` (`pip install kaleido`). Se manca, l’app lo segnala.

---

## 7. Riassunto veloce

| Cosa vuoi fare              | Dove andare / Cosa usare                    |
|----------------------------|--------------------------------------------|
| Cambiare energia/materiale/spessore | Barra laterale sinistra                    |
| Vedere trasmissione e curve         | Tab “Grafici”, metriche in alto            |
| Confrontare materiali              | Tab “Dati”, tabella confronto               |
| Simulare a caso (Monte Carlo)      | Barra laterale → “Esegui simulazione Monte Carlo” |
| Scaricare un grafico               | Pulsanti sotto il grafico (PNG/PDF)        |

---

## Avvertenza

GammaLab usa **modelli semplificati** a scopo didattico. **Non** va usato per applicazioni cliniche, ingegneristiche o di sicurezza. Per calcoli reali servono banche dati (es. NIST) e strumenti professionali.
