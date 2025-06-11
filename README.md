# Uvod u teoriju računarstva - Laboratorijske vježbe

Ovaj repozitorij sadrži programska ostvarenja laboratorijskih vježbi iz predmeta Uvod u teoriju računarstva. Svaka vježba implementirana je u programskom jeziku Python i smještena je u zasebnom direktoriju.

## Struktura Repozitorija

Repozitorij je podijeljen u četiri glavna direktorija, svaki posvećen jednoj laboratorijskoj vježbi:

- **1-NFA-with-eps-transitions**: Simulator nedeterminističkog konačnog automata (NKA) s epsilon-prijelazima.
- **2-DFA**: Minimizacija determinističkog konačnog automata (DKA).
- **3-Pushdown-automata**: Simulator determinističkog potisnog automata (DPA) koji nizove prihvaća prihvatljivim stanjem.
- **4-Recursive-descent-parser**: Parser tehnikom rekurzivnog spusta.

Svako kazalo sadrži sljedeće:

- **Glavnu skriptu**: Implementaciju zadatka laboratorijske vježbe.
- `runtests.sh`: Skriptu za pokretanje testova.
- `testovi/`: Kazalo s testnim datotekama za provjeru ispravnosti implementacije.

## Pokretanje Testova

Za pokretanje testova za svaku pojedinu laboratorijsku vježbu, postavi se u odgovarajuće kazalo te izvrši skriptu `runtests.sh`. Primjer pokretanja prve lab. vježbe:

```bash
git clone https://github.com/domamaric/UTR.git
cd UTR/1-NFA-with-eps-transitions && ./runtests.sh
```
