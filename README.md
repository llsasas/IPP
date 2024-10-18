# Projekt do IPP 2023/24
Tento repozitář obsahuje dva hlavní soubory pro projekt do předmětu **IPP** na FIT VUT, a to:
- `parser.py`: Analyzátor zdrojového kódu jazyka IPPcode23
- `interpret.py`: Interpret zdrojového kódu jazyka IPPcode23
- `ZADANI.pdf`: Dokument se zadáním projektu

## Autor
- Samuel Čus - xcussa00@vutbr.cz

## Popis

### `parser.py`
Analyzátor čte zdrojový kód jazyka IPPcode23, kontroluje jeho lexikální a syntaktickou správnost a generuje výstup ve formátu XML. Kód je zpracováván po řádcích, odstraňují se komentáře a kontrolují se typy a počty operandů. V případě nalezení chyby program vrací odpovídající návratový kód.

### `interpret.py`
Interpret slouží k provedení kódu v jazyce IPPcode23. Načítá instrukce, zpracovává je a provádí s ohledem na jejich operační kódy. Pokud je během zpracování nalezena chyba, program se ukončí s chybovým kódem.

## Překlad a spuštění
Pro spuštění `parser.py` a `interpret.py` použijte následující příkaz:

```bash
python3 parser.py <input_file>
python3 interpret.py <xml_input_file>
