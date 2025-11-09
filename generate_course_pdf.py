"""Generate an automatic PDF course booklet.

This script creates a multi-page PDF course.  By default it builds a
70-page "Curs Python Începători" booklet containing a structured
curriculum, learning objectives, practice exercises, and resources for
self-study.  The output PDF is ready to be shared with students or used
as a starting point for a personalized training manual.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence
import argparse
import textwrap

from fpdf import FPDF


@dataclass
class Lesson:
    """Represents a single lesson page in the course."""

    module_number: int
    module_title: str
    lesson_number: int
    lesson_title: str
    learning_objectives: Sequence[str]
    key_concepts: Sequence[str]
    practice_ideas: Sequence[str]
    resources: Sequence[str]
    summary: str

    @property
    def header(self) -> str:
        return f"Modulul {self.module_number}: {self.module_title}"

    @property
    def full_title(self) -> str:
        return f"Lecția {self.lesson_number}: {self.lesson_title}"


class CoursePDF(FPDF):
    """Custom PDF builder with helper methods for consistent styling."""

    def header(self) -> None:  # type: ignore[override]
        if hasattr(self, "course_title"):
            self.set_font("Helvetica", "B", 12)
            self.cell(0, 10, getattr(self, "course_title"), 0, 1, "C")
            self.ln(2)

    def footer(self) -> None:  # type: ignore[override]
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120)
        self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")


def wrap_text(text: str) -> str:
    """Wrap text at 95 characters for better PDF formatting."""

    return "\n".join(textwrap.wrap(text, width=95))


def build_lessons() -> List[Lesson]:
    """Return the default 70 lesson descriptions."""

    modules = [
        (
            "Introducere în Python",
            "Acest modul pune bazele cursului și creează un vocabular comun pentru toți participanții.",
            [
                (
                    "De ce să înveți Python",
                    [
                        "Identifică avantajele limbajului în raport cu alte opțiuni",
                        "Descoperă zonele în care Python este lider de piață",
                        "Definește obiective personale de învățare pentru următoarele săptămâni",
                    ],
                    [
                        "Simplitate, comunitate, ecosistem bogat",
                        "Proiecte posibile: web, automatizări, analiză de date",
                        "Caracteristici de design care ușurează învățarea",
                    ],
                    [
                        "Scrie o listă cu patru motive pentru care dorești să înveți Python",
                        "Caută trei proiecte open-source românești scrise în Python",
                        "Compară sintaxa Python cu alt limbaj cunoscut și notează diferențele",
                    ],
                ),
                (
                    "Instalare și configurare",
                    [
                        "Instalează interpretorul Python pe orice sistem de operare",
                        "Configurează un editor cu suport pentru Python și linting",
                        "Testează mediul rulând un program de bază",
                    ],
                    [
                        "Distribuții oficiale și alternative precum Anaconda",
                        "Folosirea terminalului versus IDE",
                        "Verificarea versiunii și a variabilei PATH",
                    ],
                    [
                        "Instalează Python 3.x și confirmă versiunea în terminal",
                        "Configurează Visual Studio Code cu extensiile recomandate",
                        "Creează un fișier hello_world.py și rulează-l",
                    ],
                ),
                (
                    "Prima rulare și interfața REPL",
                    [
                        "Folosirea interactivă a interpretorului pentru experimente rapide",
                        "Tipuri de erori și cum să le citești",
                        "Importul modulelor standard direct din REPL",
                    ],
                    [
                        "Promptul >>> și istoria comenzilor",
                        "Funcția help() și documentația din Python",
                        "Stocarea rezultatelor în variabile temporare",
                    ],
                    [
                        "Rulează câteva operații matematice în REPL",
                        "Folosește funcția help(int) pentru a citi documentația",
                        "Salvează o sesiune interesantă în istoricul terminalului",
                    ],
                ),
                (
                    "Structura unui script Python",
                    [
                        "Diferențiază rularea din fișiere și interactiv",
                        "Descrie secvența execuției într-un fișier",
                        "Documentează codul cu docstring-uri și comentarii",
                    ],
                    [
                        "Shebang, encoding și moduri de rulare",
                        "Importuri și organizarea logică a codului",
                        "Ciclul editare-rulare-analiză",
                    ],
                    [
                        "Scrie un script cu o funcție main simplă",
                        "Adaugă comentarii explicative pentru fiecare secțiune",
                        "Rulează scriptul din terminal cu argumente",
                    ],
                ),
                (
                    "Tipuri de date de bază",
                    [
                        "Lucrează cu numere, stringuri și valori booleene",
                        "Transformă valori între tipuri diferite",
                        "Evaluează expresii simple și prioritizează operații",
                    ],
                    [
                        "Integers vs floats și operațiile suportate",
                        "Stringuri și metodele comune",
                        "Adevăr și fals, operatori logici",
                    ],
                    [
                        "Crează o scurtă fișă cu exemple de conversie",
                        "Testează metode precum upper(), replace(), split()",
                        "Construiește expresii complexe cu operatori logici",
                    ],
                ),
                (
                    "Variabile și stil",
                    [
                        "Denumește variabile conform convențiilor PEP 8",
                        "Explică diferența dintre mutabilitate și imutabilitate",
                        "Folosește tipizarea statică prin hinturi acolo unde ajută",
                    ],
                    [
                        "naming, tipuri și reasignare",
                        "Seturi de bune practici în comunitatea Python",
                        "Tipuri built-in și modul typing",
                    ],
                    [
                        "Refactorizează nume slabe într-un script dat",
                        "Testează efectul operatorului id asupra variabilelor",
                        "Adaugă type hints într-o funcție și rulează mypy",
                    ],
                ),
                (
                    "Resurse și comunitate",
                    [
                        "Identifică principalele surse de documentare",
                        "Explică modul în care comunitatea contribuie la pachete",
                        "Planifică o strategie de învățare pe termen lung",
                    ],
                    [
                        "python.org, PEP-uri și standarde",
                        "Stack Overflow, PyCon, meetup-uri locale",
                        "Tutoriale gratuite vs cursuri structurate",
                    ],
                    [
                        "Înscrie-te pe un forum sau grup de discuții",
                        "Adaugă în calendar două evenimente relevante",
                        "Selectează o carte sau un curs video și planifică studiul",
                    ],
                ),
            ],
        ),
        (
            "Controlul fluxului",
            "Instrucțiunile de control oferă structura logică necesară pentru orice program.",
            [
                (
                    "Instrucțiuni condiționale",
                    [
                        "Scrie condiții compuse cu operatori logici",
                        "Aplică sintaxa if/elif/else în programe reale",
                        "Gestionează cazuri neprevăzute cu ramuri implicite",
                    ],
                    [
                        "Comparatori, operatorul ternar și pattern matching",
                        "Truthy și falsy în expresii",
                        "Arhitecturi de decizie clar structurate",
                    ],
                    [
                        "Rescrie un set de reguli de business folosind if",
                        "Analizează cod pentru a elimina ramuri redundante",
                        "Creează un validator cu mesaje clare pentru fiecare ramură",
                    ],
                ),
                (
                    "Bucla while",
                    [
                        "Identifică situații potrivite pentru bucle controlate de condiții",
                        "Previne buclele infinite folosind opriri clare",
                        "Folosește instrucțiunile break și continue responsabil",
                    ],
                    [
                        "Structura buclelor while",
                        "Verificări înainte și după buclă",
                        "Exemple comune: meniuri interactive, așteptarea input-ului",
                    ],
                    [
                        "Construiește un joc de ghicit numere folosind while",
                        "Analizează o buclă problematică și corecteaz-o",
                        "Transformă o repetare manuală într-o buclă while",
                    ],
                ),
                (
                    "Bucla for și iterabilele",
                    [
                        "Lucrează cu range și colecții iterate",
                        "Folosește enumerate și zip pentru iterare sincronizată",
                        "Creează list comprehensions eficiente",
                    ],
                    [
                        "Iterabile, iteratori și protocolul for",
                        "Pattern-uri cu comprehensions și generatori",
                        "Funcții ajutătoare din modulul itertools",
                    ],
                    [
                        "Transformă un set de bucle while în for",
                        "Optimizează procesarea unei liste cu comprehensions",
                        "Experimentează cu map, filter și generator expressions",
                    ],
                ),
                (
                    "Introducere în erori și excepții",
                    [
                        "Înțelege diferența dintre erori de sintaxă și de runtime",
                        "Aplică blocurile try/except pentru a controla erorile",
                        "Creează excepții personalizate pentru scenarii specifice",
                    ],
                    [
                        "Ierarhia excepțiilor built-in",
                        "Clauze finally și else",
                        "Logarea și raportarea erorilor",
                    ],
                    [
                        "Scrie un parser simplu cu tratament de erori",
                        "Extinde o aplicație existentă cu excepții custom",
                        "Testează cum se propagă o excepție neinterceptată",
                    ],
                ),
                (
                    "Introducere în debugging",
                    [
                        "Folosește print debugging, logging și pdb",
                        "Planifică strategii pentru identificarea bug-urilor",
                        "Aplică debugging pas cu pas într-un IDE",
                    ],
                    [
                        "Tipuri de bug-uri și abordări sistematice",
                        "Instrumente precum breakpoint(), pdb, VS Code debugger",
                        "Importanța testelor și a jurnalizării",
                    ],
                    [
                        "Instrumentează un script cu logging de bază",
                        "Rezolvă trei bug-uri deliberate dintr-un fișier demonstrativ",
                        "Documentează pașii urmați într-un jurnal de debugging",
                    ],
                ),
                (
                    "Mini-proiect: calculator de buget",
                    [
                        "Aplică deciziile și buclele pentru a automatiza calcule",
                        "Lucrează cu input-ul utilizatorului în mod sigur",
                        "Construiște rapoarte simple în consolă",
                    ],
                    [
                        "Organizarea logicii într-un script coerent",
                        "Validarea datelor introduse",
                        "Raportare și formatări prietenoase",
                    ],
                    [
                        "Planifică și scrie un plan de test pentru aplicație",
                        "Extinde aplicația pentru a suporta categorii dinamice",
                        "Adaugă salvarea rezultatelor într-un fișier text",
                    ],
                ),
                (
                    "Recapitulare și evaluare",
                    [
                        "Revizuiește toate conceptele cheie din modul",
                        "Exersează transformarea cerințelor în cod",
                        "Identifică zone ce necesită clarificări suplimentare",
                    ],
                    [
                        "Grilă de verificare a cunoștințelor",
                        "Tipuri de întrebări frecvente la interviuri junior",
                        "Lista de resurse pentru aprofundare",
                    ],
                    [
                        "Completează un chestionar de auto-evaluare",
                        "Rezolvă exerciții suplimentare cu bucle",
                        "Pregătește întrebări pentru sesiunea de Q&A",
                    ],
                ),
            ],
        ),
    ]

    # Additional modules definition continues below
    additional_modules = [
        (
            "Funcții și organizarea codului",
            "Funcțiile permit reutilizarea codului și fac programele mai ușor de testat.",
            [
                (
                    "Definirea funcțiilor",
                    [
                        "Creează funcții cu și fără valori returnate",
                        "Documentează parametri și rezultatele",
                        "Evaluează efectele secundare ale funcțiilor",
                    ],
                    [
                        "Sintaxa def, return și docstring",
                        "Parametri poziționali și numiți",
                        "Valori implicite și argumente variadice",
                    ],
                    [
                        "Scrie funcții care procesează liste",
                        "Transformă cod duplicat într-o funcție reutilizabilă",
                        "Analizează modul în care return influențează fluxul",
                    ],
                ),
                (
                    "Argumente și tipizare",
                    [
                        "Explică diferența dintre *args și **kwargs",
                        "Aplică type hints pentru claritate",
                        "Utilizează dataclasses pentru structuri simple",
                    ],
                    [
                        "Ordonarea argumentelor",
                        "Typing.Optional, Union și Literal",
                        "Avantajele dataclasses față de tuple",
                    ],
                    [
                        "Extinde o funcție existentă cu argumente opționale",
                        "Adaugă type hints și rulează un checker",
                        "Transformă un tuple într-o dataclass",
                    ],
                ),
                (
                    "Programare funcțională",
                    [
                        "Folosește funcții ca valori de primă clasă",
                        "Aplică map, filter și reduce",
                        "Construiește generatoare eficiente",
                    ],
                    [
                        "Lambda expressions și closures",
                        "Modulele functools și itertools",
                        "Beneficii și limitări ale stilului funcțional",
                    ],
                    [
                        "Optimizează un flux de date folosind map/filter",
                        "Rescrie o buclă folosind un generator",
                        "Experimentează cu decorators simpli",
                    ],
                ),
                (
                    "Testarea funcțiilor",
                    [
                        "Scrie teste unitare pentru funcții",
                        "Folosește assert și pytest",
                        "Acoperă cazuri de margine și input invalid",
                    ],
                    [
                        "Structura unui test unit",
                        "Fixtures și parametrizări în pytest",
                        "Integrarea testelor în procesul de dezvoltare",
                    ],
                    [
                        "Scrie teste pentru cel puțin trei funcții",
                        "Rulează pytest și interpretează rezultatele",
                        "Configurează un workflow de testare automată",
                    ],
                ),
                (
                    "Documentarea codului",
                    [
                        "Creează docstring-uri conforme PEP 257",
                        "Generează documentație automată",
                        "Folosește comentarii doar când este necesar",
                    ],
                    [
                        "Formate Google, NumPy și reStructuredText",
                        "Sphinx, MkDocs și alte generatoare",
                        "Instrumente pentru verificarea documentației",
                    ],
                    [
                        "Adaugă docstring-uri într-un proiect existent",
                        "Configurează Sphinx pentru un proiect mic",
                        "Publică documentația local sau online",
                    ],
                ),
                (
                    "Structurarea proiectelor",
                    [
                        "Organizează fișierele în module și pachete",
                        "Folosește __init__.py pentru exporturi",
                        "Planifică un layout scalabil pentru proiecte",
                    ],
                    [
                        "Structuri standard de directoare",
                        "Importuri relative și absolute",
                        "Rolul setup.cfg și pyproject.toml",
                    ],
                    [
                        "Reorganizează un proiect monolit într-un pachet",
                        "Analizează diagrame de module pentru claritate",
                        "Pregătește proiectul pentru publicare pe PyPI",
                    ],
                ),
                (
                    "Revizuire modul",
                    [
                        "Recapitulează cele mai utile pattern-uri de funcții",
                        "Stabilește pași pentru menținerea calității codului",
                        "Pregătește un cheat sheet personalizat",
                    ],
                    [
                        "Sinteza conceptelor și legături cu module viitoare",
                        "Checklist pentru code review",
                        "Resurse pentru aprofundarea conceptelor avansate",
                    ],
                    [
                        "Creează un cheat sheet de o pagină",
                        "Realizează un mini proiect folosind funcții",
                        "Împărtășește notițele într-un repo personal",
                    ],
                ),
            ],
        ),
        (
            "Colecții și structuri de date",
            "Colecțiile din Python facilitează stocarea și procesarea eficientă a datelor.",
            [
                (
                    "Liste și operații",
                    [
                        "Creează, modifică și iterează liste",
                        "Aplică slicing și comprehensions",
                        "Optimizează pentru performanță și claritate",
                    ],
                    [
                        "Metodele listelor și pattern-uri de utilizare",
                        "List vs tuple vs array",
                        "Impactul mutabilității asupra bug-urilor",
                    ],
                    [
                        "Rescrie cod pentru a folosi comprehensions",
                        "Analizează complexitatea unor operații pe listă",
                        "Creează liste imbricate pentru tabele",
                    ],
                ),
                (
                    "Tuple și seturi",
                    [
                        "Folosește tuple pentru date imuabile",
                        "Aplică seturi pentru elemente unice",
                        "Transformă între liste, seturi și tuple",
                    ],
                    [
                        "Proprietăți matematice ale seturilor",
                        "Dezavantaje și avantaje ale tuplelor",
                        "Frozen set și aplicații",
                    ],
                    [
                        "Modelează coordonate sau evenimente cu tuple",
                        "Curăță duplicate dintr-o listă mare",
                        "Compară timpii de acces pentru liste și seturi",
                    ],
                ),
                (
                    "Dicționare și mapări",
                    [
                        "Creează dicționare cu chei diferite",
                        "Gestionează accesul sigur cu get și setdefault",
                        "Folosește dict comprehensions și JSON",
                    ],
                    [
                        "Metode utile: items, keys, values",
                        "OrderedDict și defaultdict",
                        "Serializarea în JSON și YAML",
                    ],
                    [
                        "Construiește un index pentru un set de date",
                        "Conversie JSON ↔ dict pentru API-uri",
                        "Creează rapoarte simple pe baza unui dicționar",
                    ],
                ),
                (
                    "Structuri din collections",
                    [
                        "Aplică namedtuple, deque și Counter",
                        "Selectează structura potrivită pentru probleme",
                        "Integrează structuri hibride în proiecte",
                    ],
                    [
                        "Beneficiile modulelor din biblioteca standard",
                        "Când să folosești pachete externe",
                        "Considerente de performanță și memorie",
                    ],
                    [
                        "Implementează un histogram folosind Counter",
                        "Modelează o coadă de job-uri cu deque",
                        "Compară namedtuple cu dataclass",
                    ],
                ),
                (
                    "Lucrul cu date tabulare",
                    [
                        "Importă date din fișiere CSV",
                        "Curăță și normalizează datele",
                        "Generează statistici descriptive simple",
                    ],
                    [
                        "Modulele csv și pathlib",
                        "List comprehensions pentru transformare",
                        "Introducere în pandas pentru începători",
                    ],
                    [
                        "Construiește un script de raportare din CSV",
                        "Scrie funcții pentru validarea datelor",
                        "Importă date într-un DataFrame și salvează rezultate",
                    ],
                ),
                (
                    "Algoritmi de bază",
                    [
                        "Implementă căutări și sortări simple",
                        "Analizează complexitatea timp/spațiu",
                        "Compară implementări built-in cu cele manuale",
                    ],
                    [
                        "Bubble sort, selection sort și alternative",
                        "Căutare liniară vs binară",
                        "Instrumente pentru măsurarea performanței",
                    ],
                    [
                        "Implementează și testează două algoritmi de sortare",
                        "Compară timpii folosind timeit",
                        "Documentează avantajele fiecărui algoritm",
                    ],
                ),
                (
                    "Recapitulare colecții",
                    [
                        "Rezolvă probleme care combină multiple structuri",
                        "Analizează modul în care alegerea structurii afectează codul",
                        "Pregătește proiecte bazate pe date",
                    ],
                    [
                        "Pattern-uri comune în procesarea datelor",
                        "Erori frecvente și cum le eviți",
                        "Resurse pentru aprofundare: pandas, numpy",
                    ],
                    [
                        "Rezolvă provocări de pe platforme online",
                        "Întocmește un glosar de termeni despre colecții",
                        "Scrie un eseu scurt despre importanța structurilor corecte",
                    ],
                ),
            ],
        ),
    ]

    more_modules = [
        (
            "Lucrul cu fișiere și date",
            "Manipularea fișierelor este esențială pentru aplicații orientate pe date.",
            [
                (
                    "Citirea și scrierea fișierelor text",
                    [
                        "Deschide fișiere folosind context managers",
                        "Gestionează encoding-uri și erori",
                        "Procesează fișiere linie cu linie",
                    ],
                    [
                        "Funcția open și modurile de lucru",
                        "with statement și cleanup automat",
                        "Scrierea formatată cu template-uri",
                    ],
                    [
                        "Creează un jurnal zilnic automatizat",
                        "Analizează un fișier log și extrage informații",
                        "Scrie un raport în format Markdown",
                    ],
                ),
                (
                    "Fișiere binare și imagini",
                    [
                        "Diferențiază între text și binar",
                        "Folosește modul struct pentru date binare",
                        "Manipulează imagini cu biblioteci terțe",
                    ],
                    [
                        "Bites versus bytes și importanța offset-urilor",
                        "Serializarea datelor binare",
                        "Pillow și alte biblioteci pentru imagini",
                    ],
                    [
                        "Scrie un script care citește metadata din imagini",
                        "Transformă un fișier binar într-un format custom",
                        "Compară dimensiunea fisierelor text și binare",
                    ],
                ),
                (
                    "CSV, JSON și YAML",
                    [
                        "Importă și exportă date structurate",
                        "Mapează câmpuri către obiecte Python",
                        "Validează schema datelor",
                    ],
                    [
                        "Modulele csv, json și yaml",
                        "Gestionarea datelor lipsă",
                        "Conversii între formate",
                    ],
                    [
                        "Construiește un convertor CSV → JSON",
                        "Definește o schemă și validează datele",
                        "Creează un script de backup pentru configurații",
                    ],
                ),
                (
                    "Persistență cu SQLite",
                    [
                        "Creează baze de date și tabele",
                        "Execută interogări și tranzacții",
                        "Integrează baza de date într-o aplicație",
                    ],
                    [
                        "sqlite3 și context managers",
                        "Modelarea datelor relaționale",
                        "Pattern-uri de acces la date",
                    ],
                    [
                        "Proiectează o schemă pentru o aplicație TODO",
                        "Implementează operații CRUD",
                        "Scrie teste pentru funcțiile de acces la date",
                    ],
                ),
                (
                    "Lucrul cu API-uri",
                    [
                        "Consumă servicii REST folosind requests",
                        "Gestionează autentificarea și erorile",
                        "Transformă răspunsurile în rapoarte utile",
                    ],
                    [
                        "Metode HTTP și status codes",
                        "Pagini, rate limiting și caching",
                        "Prelucrarea JSON și gestionarea erorilor",
                    ],
                    [
                        "Creează un client simplu pentru o API publică",
                        "Gestionează erorile într-un wrapper de API",
                        "Creează diagrame din datele preluate",
                    ],
                ),
                (
                    "Automatizări cu scripturi",
                    [
                        "Planifică task-uri repetitive",
                        "Rulează scripturi cu argumente",
                        "Folosește logging pentru monitorizare",
                    ],
                    [
                        "argparse și click",
                        "Programarea task-urilor cu cron",
                        "Logare, notificări și rapoarte",
                    ],
                    [
                        "Automatizează organizarea fișierelor dintr-un director",
                        "Creează un script pentru backup incremental",
                        "Configurează notificări prin email pentru un job",
                    ],
                ),
                (
                    "Revizuire și proiect",
                    [
                        "Integrează tot ce ai învățat într-o aplicație completă",
                        "Documentează procesul de lucru",
                        "Prezintă rezultatele și învață din feedback",
                    ],
                    [
                        "Proiecte bazate pe date și API-uri",
                        "Scrierea unei documentații tehnice",
                        "Prezentarea proiectului în fața colegilor",
                    ],
                    [
                        "Construiște o aplicație de agregare știri",
                        "Scrie un jurnal tehnic al deciziilor",
                        "Organizează o sesiune demo pentru proiect",
                    ],
                ),
            ],
        ),
        (
            "Programare orientată pe obiect",
            "OOP oferă instrumentele pentru a modela aplicații complexe și extensibile.",
            [
                (
                    "Clase și obiecte",
                    [
                        "Definește clase cu atribute și metode",
                        "Creează instanțe și gestionează starea",
                        "Folosește __init__ pentru inițializare",
                    ],
                    [
                        "Diferența dintre clasă și obiect",
                        "Self și variabile de instanță",
                        "Reprezentări string ale obiectelor",
                    ],
                    [
                        "Modelează un obiect real folosind o clasă",
                        "Adaugă metode pentru operațiuni cheie",
                        "Implementează __str__ și __repr__",
                    ],
                ),
                (
                    "Încapsulare și proprietăți",
                    [
                        "Protejează starea internă a obiectelor",
                        "Folosește property pentru acces controlat",
                        "Documentează contractele publice",
                    ],
                    [
                        "Atribute private și convenții",
                        "Getter, setter și property",
                        "Beneficiile încapsulării",
                    ],
                    [
                        "Transformă variabile publice în proprietăți",
                        "Adaugă validări în setter",
                        "Documentează API-ul public al unei clase",
                    ],
                ),
                (
                    "Moștenire și compoziție",
                    [
                        "Alege între moștenire și compoziție",
                        "Extinde clase existente fără a le modifica",
                        "Aplică principiile SOLID pentru ierarhii",
                    ],
                    [
                        "Inheritance în Python și super()",
                        "Compoziție pentru comportamente reutilizabile",
                        "Pattern-uri precum mixin",
                    ],
                    [
                        "Creează o ierarhie de clase pentru vehicule",
                        "Refactorizează o moștenire multiplă problematică",
                        "Aplică compoziția pentru a evita duplicarea",
                    ],
                ),
                (
                    "Metode speciale și operatori",
                    [
                        "Implementează metode speciale pentru integrare cu Python",
                        "Personalizează operatori și protocoluri",
                        "Utilizează context managers personalizați",
                    ],
                    [
                        "__str__, __repr__, __len__, __enter__/__exit__",
                        "Protocolul iteratorilor și operator overloading",
                        "Contextlib pentru resurse",
                    ],
                    [
                        "Adaugă iterație personalizată unei clase",
                        "Creează un context manager pentru fișiere temporare",
                        "Suprascrie operatori pentru un model matematic",
                    ],
                ),
                (
                    "Principii SOLID",
                    [
                        "Descrie cele cinci principii SOLID",
                        "Aplică aceste principii la clase existente",
                        "Identifică mirosuri de design",
                    ],
                    [
                        "Single Responsibility și Open/Closed",
                        "Liskov, Segregarea interfețelor, Dependency inversion",
                        "Analiza codului existent",
                    ],
                    [
                        "Analizează un proiect și identifică încălcări",
                        "Propune refactorizări pentru respectarea principiilor",
                        "Documentează schimbările și justificările",
                    ],
                ),
                (
                    "Design Patterns",
                    [
                        "Învață pattern-uri fundamentale în Python",
                        "Selectează pattern-ul potrivit pentru o problemă",
                        "Analizează compromisuri între soluții",
                    ],
                    [
                        "Singleton, Factory, Strategy, Observer",
                        "Implementări idiomatice în Python",
                        "Când să eviți pattern-uri complicate",
                    ],
                    [
                        "Implementează două pattern-uri într-un proiect existent",
                        "Compară implementarea Python cu alte limbaje",
                        "Prezintă exemple reale de pattern-uri",
                    ],
                ),
                (
                    "OOP în proiecte reale",
                    [
                        "Integrează OOP cu testarea și documentarea",
                        "Planifică extensibilitatea din timp",
                        "Folosește dataclasses și attrs pentru modele",
                    ],
                    [
                        "Arhitectura aplicațiilor orientate pe obiect",
                        "Refactorizare incrementală",
                        "Instrumente pentru generarea de diagrame UML",
                    ],
                    [
                        "Refactorizează un modul procedural folosind OOP",
                        "Scrie teste pentru clase și interacțiuni",
                        "Generează diagrame UML folosind plantuml",
                    ],
                ),
            ],
        ),
        (
            "Module și pachete",
            "Înțelegerea ecosistemului de pachete accelerează dezvoltarea.",
            [
                (
                    "Gestionarea dependențelor",
                    [
                        "Foloseste pip și virtual environments",
                        "Creează fișiere requirements",
                        "Documentează pașii de instalare",
                    ],
                    [
                        "python -m venv și pip",
                        "pip-tools și poetry",
                        "Documentarea instalării",
                    ],
                    [
                        "Creează un mediu virtual pentru un proiect",
                        "Generează un requirements.txt coerent",
                        "Documentează procesul în README",
                    ],
                ),
                (
                    "Explorarea bibliotecii standard",
                    [
                        "Identifică module utile pentru sarcini comune",
                        "Folosește pathlib, datetime și logging",
                        "Aplică modulul argparse în scripturi",
                    ],
                    [
                        "Module mai puțin cunoscute dar utile",
                        "Bune practici în importuri",
                        "Documentarea modulelor",
                    ],
                    [
                        "Creează un ghid al modulelor preferate",
                        "Scrie exemple practice pentru trei module",
                        "Documentează un pattern cu logging",
                    ],
                ),
                (
                    "Pachete terțe populare",
                    [
                        "Evaluează calitatea pachetelor",
                        "Instalează și folosește requests, pandas, click",
                        "Verifică licențele și starea proiectului",
                    ],
                    [
                        "PyPI și criterii de selecție",
                        "Documentație și suport",
                        "Integrare în proiecte existente",
                    ],
                    [
                        "Compară două pachete care rezolvă aceeași problemă",
                        "Scrie un scurt tutorial pentru un pachet ales",
                        "Evaluează popularitatea folosind date PyPI",
                    ],
                ),
                (
                    "Publicarea unui pachet",
                    [
                        "Structurează proiectul pentru distribuție",
                        "Configurați metadata și build-ul",
                        "Publică pachetul pe TestPyPI",
                    ],
                    [
                        "pyproject.toml, setup.cfg și wheel",
                        "Licențiere și versionare semantică",
                        "Continuous Integration pentru pachete",
                    ],
                    [
                        "Configurează un proiect pentru publicare",
                        "Generează un wheel local și testează instalarea",
                        "Publică pachetul pe TestPyPI folosind token",
                    ],
                ),
                (
                    "Securitate și întreținere",
                    [
                        "Actualizează dependențele în siguranță",
                        "Scanează vulnerabilități în proiect",
                        "Monitorizează release-urile critice",
                    ],
                    [
                        "pip-audit și safety",
                        "Dependabot și alerte",
                        "Procese de mentenanță",
                    ],
                    [
                        "Rulează pip-audit pe un proiect personal",
                        "Planifică o strategie de update periodic",
                        "Documentează un incident simulat și rezolvarea lui",
                    ],
                ),
                (
                    "Crearea unui CLI profesional",
                    [
                        "Aplică click sau typer pentru aplicații robuste",
                        "Gestionează subcomenzi și validări",
                        "Scrie documentație și mesaje de ajutor",
                    ],
                    [
                        "Pattern-uri pentru CLI-uri",
                        "Testarea aplicațiilor de linie de comandă",
                        "Distribuirea CLI-urilor",
                    ],
                    [
                        "Construiește un CLI care orchestrează un workflow",
                        "Testează CLI-ul folosind pytest",
                        "Documentează exemple de utilizare",
                    ],
                ),
                (
                    "Recapitulare module și pachete",
                    [
                        "Sintetizează procesul de creare și menținere",
                        "Planifică contribuții la proiecte open source",
                        "Defineste un plan de creștere profesională",
                    ],
                    [
                        "Checklist pentru lansarea unui pachet",
                        "Ghid pentru contribuții sănătoase",
                        "Comunități și oportunități",
                    ],
                    [
                        "Propune o idee de pachet open source",
                        "Creează un roadmap public",
                        "Împărtășește planul cu mentorul sau colegii",
                    ],
                ),
            ],
        ),
        (
            "Testare și calitate",
            "Testarea asigură stabilitatea și încrederea în cod.",
            [
                (
                    "Noțiuni introductive despre testare",
                    [
                        "Clasifică tipurile de teste",
                        "Explică piramida testării",
                        "Alege instrumentele potrivite",
                    ],
                    [
                        "Testare manuală vs automată",
                        "Rolul QA și al dezvoltatorilor",
                        "Beneficii ale testelor timpurii",
                    ],
                    [
                        "Elaborează un plan de test pentru un proiect existent",
                        "Evaluează acoperirea actuală",
                        "Propune îmbunătățiri ale procesului",
                    ],
                ),
                (
                    "Testare unit cu pytest",
                    [
                        "Scrie teste izolate pentru funcții",
                        "Folosește fixtures pentru setup",
                        "Rulează teste cu markeri",
                    ],
                    [
                        "pytest.ini și structura directoarelor",
                        "Fixtures reutilizabile",
                        "Markeri custom și skip",
                    ],
                    [
                        "Scrie trei teste unitare pentru un modul",
                        "Creează fixture pentru resurse comune",
                        "Folosește markeri pentru a categoriza testele",
                    ],
                ),
                (
                    "Testare de integrare",
                    [
                        "Simulează colaborarea dintre module",
                        "Configurează medii de test",
                        "Folosește mocking pentru dependențe",
                    ],
                    [
                        "Diferențe față de testele unitare",
                        "Instrumente precum responses și pytest-mock",
                        "Strategii pentru testarea API-urilor",
                    ],
                    [
                        "Scrie teste pentru o funcție care apelează un API",
                        "Construiește un fișier docker-compose pentru testare",
                        "Analizează logurile pentru a identifica probleme",
                    ],
                ),
                (
                    "Testare automată în CI",
                    [
                        "Integrează testele într-un pipeline GitHub Actions",
                        "Configurează badge-uri și rapoarte",
                        "Gestionează testele instabile",
                    ],
                    [
                        "yml pentru workflows",
                        "Raportare cu coverage",
                        "Strategii de retry și flakiness",
                    ],
                    [
                        "Configurează un workflow CI complet",
                        "Adaugă rapoarte HTML pentru coverage",
                        "Documentează modul de interpretare a rezultatelor",
                    ],
                ),
                (
                    "Revizuiri de cod și calitate",
                    [
                        "Aplică code review constructiv",
                        "Folosește lintere și formattere",
                        "Monitorizează indicatori de calitate",
                    ],
                    [
                        "PEP 8, black, isort",
                        "Checklist pentru review",
                        "Metode de feedback eficient",
                    ],
                    [
                        "Configurează black într-un proiect",
                        "Participă la un code review simulativ",
                        "Stabilește un set de metrici de calitate",
                    ],
                ),
                (
                    "Testare exploratorie",
                    [
                        "Identifică scenarii neașteptate",
                        "Folosește heuristici pentru descoperirea bug-urilor",
                        "Documentează rezultatele rapid",
                    ],
                    [
                        "Turul turistic, tour of duty",
                        "Note-taking și rapoarte",
                        "Integrarea descoperirilor în backlog",
                    ],
                    [
                        "Planifică o sesiune exploratorie pentru un proiect",
                        "Documentează bug-urile într-un format clar",
                        "Prezintă concluziile echipei",
                    ],
                ),
                (
                    "Îmbunătățire continuă",
                    [
                        "Evaluează periodic procesul de testare",
                        "Colectează feedback și date",
                        "Adaptează strategia pe baza rezultatelor",
                    ],
                    [
                        "Retrospective și metrici",
                        "A/B testing pentru procese",
                        "Planuri de acțiune iterative",
                    ],
                    [
                        "Organizează o retrospectivă pentru testare",
                        "Definește indicatori pentru succes",
                        "Implementează o îmbunătățire și măsoară impactul",
                    ],
                ),
            ],
        ),
        (
            "Proiect practic",
            "Participantii aplică tot ce au învățat într-un proiect cap-coadă.",
            [
                (
                    "Planificarea proiectului",
                    [
                        "Definește obiective măsurabile",
                        "Stabilește cerințe funcționale și nefuncționale",
                        "Planifică etapele într-un roadmap",
                    ],
                    [
                        "Metodologii agile pentru proiecte mici",
                        "Instrumente de management: Trello, Jira",
                        "Estimare și prioritizare",
                    ],
                    [
                        "Creează un backlog inițial",
                        "Definește criterii de acceptare pentru user stories",
                        "Planifică livrabilele pe săptămâni",
                    ],
                ),
                (
                    "Design tehnic",
                    [
                        "Construiește diagrame de arhitectură",
                        "Alege tehnologiile auxiliare",
                        "Planifică interfețele între componente",
                    ],
                    [
                        "Diagrame UML și C4",
                        "Microservicii vs monolit",
                        "Gestionarea configurațiilor",
                    ],
                    [
                        "Desenează diagrame pentru proiect",
                        "Documentează deciziile tehnice",
                        "Definește contracte pentru API-uri interne",
                    ],
                ),
                (
                    "Implementare incrementală",
                    [
                        "Respectă planul și ajustează când este necesar",
                        "Integrează feedback rapid",
                        "Menține codul curat și testat",
                    ],
                    [
                        "Strategii de commit-uri clare",
                        "Pull request-uri mici și frecvente",
                        "Automatizarea build-ului",
                    ],
                    [
                        "Implementează primele user stories",
                        "Scrie teste automate pentru funcționalități",
                        "Cere un review tehnic după fiecare iterație",
                    ],
                ),
                (
                    "Integrare și testare",
                    [
                        "Asamblează componentele într-un întreg",
                        "Rulează testele și remediază problemele",
                        "Pregătește demonstrația finală",
                    ],
                    [
                        "CI/CD pentru proiect",
                        "Testare manuală ghidată",
                        "Observabilitate și logare",
                    ],
                    [
                        "Configurează un pipeline CI simplu",
                        "Testează scenarii cap-coadă",
                        "Documentează bug-urile întâlnite și rezolvările",
                    ],
                ),
                (
                    "Documentare și livrare",
                    [
                        "Scrie ghiduri pentru utilizatori și dezvoltatori",
                        "Pregătește prezentarea finală",
                        "Colectează feedback pentru iterații viitoare",
                    ],
                    [
                        "README, changelog și ghiduri",
                        "Structurarea prezentărilor",
                        "Gestionarea feedback-ului",
                    ],
                    [
                        "Scrie un README complet pentru proiect",
                        "Pregătește slide-uri pentru demonstrație",
                        "Adună testimoniale de la utilizatori",
                    ],
                ),
                (
                    "Reflecție și portofoliu",
                    [
                        "Analizează ce ai învățat",
                        "Identifică zone de îmbunătățire",
                        "Construiește un portofoliu convingător",
                    ],
                    [
                        "Învățare continuă și next steps",
                        "Crearea unui portofoliu",
                        "Networking și branding personal",
                    ],
                    [
                        "Scrie un studiu de caz pentru proiect",
                        "Actualizează profilurile profesionale",
                        "Planifică următoarele două proiecte personale",
                    ],
                ),
                (
                    "Pregătire pentru interviu",
                    [
                        "Conectează experiența din proiect cu cerințele joburilor",
                        "Pregătește povești STAR",
                        "Simulează interviuri tehnice",
                    ],
                    [
                        "Tipuri de întrebări tehnice și comportamentale",
                        "Metode de prezentare a proiectelor",
                        "Rolul portofoliului și al contribuțiilor publice",
                    ],
                    [
                        "Realizează un mock interview cu un coleg",
                        "Exersează prezentarea proiectului în 5 minute",
                        "Actualizează CV-ul cu rezultatele obținute",
                    ],
                ),
                (
                    "Abordare pe termen lung",
                    [
                        "Stabilește obiective SMART pentru următoarele 6 luni",
                        "Identifică mentori și comunități",
                        "Construiește un plan de învățare continuă",
                    ],
                    [
                        "Mentorat și comunități profesionale",
                        "Învățare pe tot parcursul vieții",
                        "Crearea unui brand personal",
                    ],
                    [
                        "Alege un mentor și stabilește prima întâlnire",
                        "Înscrie-te la un eveniment tehnic",
                        "Creează un plan de dezvoltare personală",
                    ],
                ),
            ],
        ),
        (
            "Pași următori",
            "Modulul final oferă resurse pentru dezvoltarea continuă.",
            [
                (
                    "Aprofundare limbaj",
                    [
                        "Identifică subiecte avansate",
                        "Planifică studii suplimentare",
                        "Stabilește obiective de nivel intermediar",
                    ],
                    [
                        "Decoratori avansați, context managers, metaclase",
                        "Recapitulare modul typing",
                        "Când să adopți un framework",
                    ],
                    [
                        "Creează o listă de cursuri avansate",
                        "Planifică un proiect open source",
                        "Documentează pașii în jurnalul de învățare",
                    ],
                ),
                (
                    "Analiză de date",
                    [
                        "Explorează ecosistemul pandas și numpy",
                        "Învață vizualizare cu matplotlib și seaborn",
                        "Planifică proiecte practice",
                    ],
                    [
                        "Fluxul tipic de analiză",
                        "Seturi de date recomandate",
                        "Biblioteci pentru machine learning",
                    ],
                    [
                        "Instalează pandas și realizează un mini-raport",
                        "Construiește grafice pentru un set de date",
                        "Încearcă un algoritm simplu din scikit-learn",
                    ],
                ),
                (
                    "Dezvoltare web",
                    [
                        "Compară framework-uri web",
                        "Construiește aplicații API și frontend",
                        "Publică aplicații în cloud",
                    ],
                    [
                        "Flask, FastAPI și Django",
                        "Templating, routing și ORM",
                        "Deploy pe Heroku, Railway, Render",
                    ],
                    [
                        "Creează un API REST cu FastAPI",
                        "Construiește un frontend simplu cu HTML și CSS",
                        "Publică aplicația pe o platformă gratuită",
                    ],
                ),
                (
                    "Automatizări și DevOps",
                    [
                        "Folosește Python pentru automatizarea infrastructurii",
                        "Învață concepte de bază DevOps",
                        "Integrează monitorizarea și alertele",
                    ],
                    [
                        "Scripturi pentru administrare",
                        "Introducere în Docker și Kubernetes",
                        "Monitorizare cu Prometheus și Grafana",
                    ],
                    [
                        "Scrie scripturi pentru gestionarea serverelor",
                        "Construiește o imagine Docker pentru un proiect",
                        "Configurează alerte pentru un serviciu",
                    ],
                ),
                (
                    "Contribuții open source",
                    [
                        "Găsește proiecte potrivite",
                        "Respectă ghidurile comunității",
                        "Gestionează PR-uri și code reviews",
                    ],
                    [
                        "good first issue și etichete similare",
                        "Procese de contribuție",
                        "Comunicare empatică",
                    ],
                    [
                        "Contribuie la documentația unui proiect",
                        "Rezolvă un bug marcat good first issue",
                        "Prezentă experiența într-un articol de blog",
                    ],
                ),
                (
                    "Construirea unei cariere",
                    [
                        "Planifică dezvoltarea profesională",
                        "Construiește rețele de contacte",
                        "Pregătește-te pentru oportunități",
                    ],
                    [
                        "Participarea la conferințe",
                        "Networking intenționat",
                        "Învățarea continuă și certificări",
                    ],
                    [
                        "Creează o listă de evenimente relevante",
                        "Pregătește un elevator pitch",
                        "Actualizează profilul LinkedIn",
                    ],
                ),
                (
                    "Menținerea motivației",
                    [
                        "Monitorizează progresul",
                        "Construiește obiceiuri sănătoase",
                        "Găsește accountability partners",
                    ],
                    [
                        "Tehnici de habit building",
                        "Instrumente pentru urmărirea progresului",
                        "Rolul comunității",
                    ],
                    [
                        "Configurează un tracker de obiceiuri",
                        "Împărtășește progresele săptămânale",
                        "Stabilește un sistem de recompense",
                    ],
                ),
                (
                    "Plan personalizat",
                    [
                        "Creează un plan de învățare pe 90 de zile",
                        "Stabilește indicatori de succes",
                        "Integrează resursele potrivite",
                    ],
                    [
                        "OKR-uri personale",
                        "Evaluare periodică",
                        "Adaptarea planului pe parcurs",
                    ],
                    [
                        "Scrie un plan detaliat în jurnal",
                        "Setează remindere pentru evaluări",
                        "Prezintă planul unui mentor pentru feedback",
                    ],
                ),
            ],
        ),
    ]

    all_modules = modules + additional_modules + more_modules

    lessons: List[Lesson] = []
    for module_index, (module_title, module_summary, lesson_specs) in enumerate(all_modules, start=1):
        for lesson_index, (lesson_title, objectives, concepts, practice) in enumerate(lesson_specs, start=1):
            lessons.append(
                Lesson(
                    module_number=module_index,
                    module_title=module_title,
                    lesson_number=lesson_index,
                    lesson_title=lesson_title,
                    learning_objectives=objectives,
                    key_concepts=concepts,
                    practice_ideas=practice,
                    resources=(
                        "Documentația oficială Python",
                        "Cartea 'Automate the Boring Stuff with Python'",
                        "Tutoriale video gratuite de pe canalul Python România",
                    ),
                    summary=module_summary,
                )
            )

    return lessons


def add_lesson_page(pdf: CoursePDF, lesson: Lesson) -> None:
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(20)
    pdf.multi_cell(0, 8, lesson.header)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(0, 7, lesson.full_title)
    pdf.ln(1)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40)
    intro = (
        f"Această lecție face parte din {lesson.header.lower()} și se concentrează pe "
        f"{lesson.lesson_title.lower()}. Scopul ei este să te ajute să aplici "
        "cunoștințele într-un context practic și să pregătești terenul pentru "
        "provocări mai avansate."
    )
    pdf.multi_cell(0, 6, wrap_text(intro))
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(10, 70, 140)
    pdf.multi_cell(0, 6, "Obiective de învățare")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40)
    for objective in lesson.learning_objectives:
        pdf.multi_cell(0, 6, f"• {objective}")
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(10, 120, 60)
    pdf.multi_cell(0, 6, "Concepte cheie")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40)
    for concept in lesson.key_concepts:
        pdf.multi_cell(0, 6, f"• {concept}")
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(160, 90, 30)
    pdf.multi_cell(0, 6, "Activități practice recomandate")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40)
    for practice in lesson.practice_ideas:
        pdf.multi_cell(0, 6, f"• {practice}")
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(120, 20, 80)
    pdf.multi_cell(0, 6, "Resurse suplimentare")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40)
    for resource in lesson.resources:
        pdf.multi_cell(0, 6, f"• {resource}")
    pdf.ln(1)

    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(90)
    pdf.multi_cell(0, 5, wrap_text(lesson.summary))


def create_course_pdf(
    lessons: Iterable[Lesson],
    output: Path,
    course_title: str,
    target_pages: int,
) -> None:
    pdf = CoursePDF()
    pdf.course_title = course_title  # type: ignore[attr-defined]
    pdf.set_auto_page_break(auto=True, margin=15)

    lessons_list = list(lessons)
    if not lessons_list:
        raise ValueError("No lessons provided to generate the PDF course.")

    # Always include a cover page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(40)
    pdf.multi_cell(0, 12, course_title, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    pdf.multi_cell(
        0,
        8,
        wrap_text(
            "Acest curs intensiv te va ghida pas cu pas prin fundamentele Python, "
            "utilizând exemple practice, activități aplicate și recomandări "
            "pentru învățare continuă. Următoarele pagini sunt structurate "
            "ca o călătorie progresivă de la noțiuni introductive până la proiecte "
            "complete."
        ),
        align="C",
    )
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 12)
    pdf.multi_cell(0, 6, "Durată recomandată: 10 săptămâni", align="C")
    pdf.multi_cell(0, 6, "Nivel: Începători motivați", align="C")

    pages_needed = max(1, target_pages - 1)  # subtract cover page

    for index in range(pages_needed):
        lesson = lessons_list[index % len(lessons_list)]
        add_lesson_page(pdf, lesson)

    output.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generează un curs PDF complet cu un singur script.",
    )
    parser.add_argument(
        "--title",
        default="Curs Python Începători",
        help="Titlul cursului afișat pe fiecare pagină.",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=70,
        help="Numărul total de pagini dorite. Include coperta.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("curs_python_incepatori.pdf"),
        help="Calea către fișierul PDF rezultat.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    lessons = build_lessons()
    create_course_pdf(lessons, output=args.output, course_title=args.title, target_pages=args.pages)
    print(f"PDF generat cu succes în {args.output.resolve()}")


if __name__ == "__main__":
    main()
