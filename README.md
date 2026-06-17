# Gamblang 🎲

Gamblang è un linguaggio di programmazione sperimentale che introduce elementi di casualità direttamente nel linguaggio. Oltre alle variabili tradizionali, supporta strutture che mantengono una cronologia dei valori assegnati e costrutti condizionali basati sulla probabilità.

Il compilatore utilizza un parser LALR per analizzare il sorgente, esegue controlli semantici sui tipi e genera codice C standard, che viene poi compilato ed eseguito tramite `gcc`.

---

## Tipi di variabili

### Variabili deterministiche (`steady`)

Le variabili `steady` si comportano come le normali variabili presenti nella maggior parte dei linguaggi.

```gamblang
steady x = 10
x = 20
```

---

### Variabili con cronologia (`gamble`)

Le variabili `gamble` memorizzano tutti i valori assegnati nel tempo. Ogni nuovo valore viene aggiunto alla cronologia usando l'operatore `<-`.

Quando la variabile viene utilizzata in un'espressione, uno dei valori salvati viene scelto casualmente.

```gamblang
gamble g <- 5
g <- 15
g <- 25

print g
```

L'output potrà essere `5`, `15` oppure `25`.

---

### Variabili probabilistiche (`coin`)

Una variabile `coin` rappresenta il risultato di un lancio probabilistico.

Il valore assegnato deve essere compreso tra `0.0` e `1.0` e indica la probabilità che la variabile assuma valore `1`.

```gamblang
coin c = 0.75
```

In questo caso `c` avrà il 75% di probabilità di valere `1` e il 25% di probabilità di valere `0`.

---

## Controllo del flusso

### Blocco `risky`

Il costrutto `risky` esegue un blocco di codice solo se un controllo probabilistico ha successo.

```gamblang
risky(0.5) do
    print "Operazione riuscita"
or do
    print "Operazione fallita"
end
```

Con probabilità `0.5` verrà eseguito il primo blocco, altrimenti il secondo.

---

### Costrutti supportati

GAMBLANG include anche:

* `if / else`
* cicli `loop ... do ... end`
* input da tastiera tramite `ask`
* operatori aritmetici
* operatori relazionali e logici

L'istruzione `ask` è consentita esclusivamente per variabili di tipo `steady`.

---

## Struttura del progetto

Il compilatore è organizzato nei seguenti moduli:

* **`gamblang`**: script di avvio del compilatore.
* **`main.py`**: parsing, analisi semantica e compilazione finale.
* **`gamblang.lark`**: grammatica del linguaggio definita con Lark.
* **`semantics.py`**: gestione della symbol table e verifica dei tipi.
* **`codegen.py`**: generazione del codice C.

---

## Come funziona

La compilazione segue questi passaggi:

1. Parsing del sorgente tramite LALR.
2. Analisi semantica e controllo dei tipi.
3. Generazione del codice C.
4. Compilazione tramite `gcc`.
5. Esecuzione del programma generato.

---

## Requisiti

* Python 3
* Lark

```bash
pip install lark
```

* GCC disponibile nel PATH di sistema

---

## Installazione

Clona il repository:

```bash
git clone https://github.com/Lucas5N/Gamblang_Staiano.git
cd Gamblang
```

Rendi eseguibile lo script principale:

```bash
chmod +x gamblang
```

---

## Utilizzo

Crea un file sorgente, ad esempio `programma.gamblang` (l'estensione non è importante), ed eseguilo con:

```bash
./gamblang programma.gamblang
```

---

## Esempio

```gamblang
steady soglia = 0.4

coin moneta = 0.65

gamble storico <- 10
storico <- 20
storico <- 30

if moneta == 1
    print "Lancio riuscito!"
    print storico
end

risky(soglia) do
    print "Operazione completata"
or do
    print "Operazione fallita"
end
```

Ogni esecuzione può produrre risultati diversi in base ai valori estratti dalle variabili `gamble` e agli eventi probabilistici generati da `coin` e `risky`.
