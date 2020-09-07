# CTRNN_Simulation_Results

## parsing batch runs

```bash
cd ../NeuroEvolution-CTRNN_new
. ~/.venv/neuro/bin/activate
python neuro_evolution_ctrnn/batch_generate_plot.py --base-dir ../CTRNN_Simulation_Results/data
cd ../CTRNN_Simulation_Results
python resuts_to_csv.py --dir data
libreoffice data.csv
```

- Dann beim csv-import dialog alle spalten markieren (strg+a) und als Spaltentyp wählen "US-Englisch"
- Ansicht-> zellen fixieren -> erste Zeile
- Daten -> sortieren 
  - schlússel 1: environment
  - schlüssel 2: max
- Alles markieren (strg-a), rechtsklick auf Spalten -> Spaltenbreite... -> 1cm
- Spaltenkopf von "plot" markieren, schrift kursiv und blau machen
- Spalte "environment": optimale spaltenbreite
 

