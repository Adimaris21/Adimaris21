# Curs Python Începători – Generator PDF

Acest repository include un script ce generează automat un curs PDF complet. Cu o singură comandă poți obține un manual structurat de 70 de pagini pentru inițierea în Python, cu obiective de învățare, concepte cheie, activități practice și resurse suplimentare.

## Cerințe

- Python 3.9 sau mai nou
- Dependențe instalate din `requirements.txt`

Instalare rapidă:

```bash
python -m venv .venv
source .venv/bin/activate  # pe Windows folosește .venv\Scripts\activate
pip install -r requirements.txt
```

## Generarea cursului PDF

Scriptul `generate_course_pdf.py` poate fi rulat direct din linia de comandă. Valorile implicite produc un document „Curs Python Începători” cu 70 de pagini (inclusiv coperta).

```bash
python generate_course_pdf.py
```

Parametrii opționali îți permit să personalizezi titlul, numărul de pagini și calea de ieșire:

```bash
python generate_course_pdf.py \
    --title "Curs Python Începători" \
    --pages 70 \
    --output materiale/curs_python.pdf
```

## Structura conținutului

Documentul generat include:

- o copertă introductivă;
- 70 de pagini cu lecții organizate pe 11 module;
- pentru fiecare lecție: obiective de învățare, concepte cheie, idei de practică și resurse recomandate;
- rezumate pentru fiecare modul și sugestii de aprofundare.

Poți modifica structura sau conținutul lecțiilor editând funcția `build_lessons()` din `generate_course_pdf.py`.

## Licență

Codul este oferit sub licență MIT. Consultă fișierul `LICENSE` (dacă există) sau adaptează-l pentru nevoile proiectului tău.
