# Re-ranking: keeping the top hybrid results

40 answerable questions, 20 hybrid candidates re-ranked by the cross-encoder, top 5 kept.

| setup | hit@5 | MRR |
|---|---|---|
| hybrid (no re-ranking) | 0.85 | 0.67 |
| re-rank, keep top 0 | 0.80 | 0.73 |
| re-rank, keep top 1 | 0.88 | 0.75 |
| re-rank, keep top 2 | 0.90 | 0.76 |
| re-rank, keep top 3 | 0.88 | 0.75 |

| # | question | hybrid (no re-ranking) | re-rank, keep top 0 | re-rank, keep top 1 | re-rank, keep top 2 | re-rank, keep top 3 |
|---|---|---|---|---|---|---|
| 1 | How many ECTS credits do I need to complete the bachelor's degree? | - | 1 | 1 | 1 | 1 |
| 2 | Wie viele Credits braucht man für den Bachelorabschluss? | - | 1 | 1 | 1 | 1 |
| 3 | How long is the internship in the practical semester? | 3 | 1 | 1 | 1 | 1 |
| 4 | Wie viele Wochen dauert das Praktikum im praktischen Studiensemester? | 1 | 1 | 1 | 1 | 1 |
| 5 | How many credits do I need before I am admitted to the internship? | 1 | 1 | 1 | 1 | 1 |
| 6 | Welche Voraussetzung gilt für die Zulassung zum Praktikum? | 2 | 1 | 1 | 1 | 1 |
| 7 | How long can I work on my bachelor's thesis? | 2 | 1 | 1 | 1 | 1 |
| 8 | Darf die Bachelorarbeit auf Englisch geschrieben werden? | 1 | 1 | 1 | 1 | 1 |
| 9 | How many hours of work does one ECTS credit correspond to? | 1 | 1 | 1 | 1 | 1 |
| 10 | What level of English do applicants need? | 1 | 1 | 1 | 1 | 1 |
| 11 | Welche Deutschkenntnisse müssen ausländische Bewerber nachweisen? | 1 | 1 | 1 | 1 | 1 |
| 12 | Which exams must be taken by the end of the second semester? | - | 1 | 1 | 1 | 1 |
| 13 | Wie viele Credits braucht man für den Eintritt in den dritten Studienabschnitt? | 1 | 1 | 1 | 1 | 1 |
| 14 | What academic degree do graduates receive? | 1 | 1 | 1 | 1 | 1 |
| 15 | How many credits is the practical semester worth? | 2 | - | - | 5 | 5 |
| 16 | Wie lange ist die Amtszeit der Prüfungskommission? | 1 | 1 | 1 | 1 | 1 |
| 17 | How many credits does the Databases module have? | 4 | - | - | - | - |
| 18 | Was ist die Regelstudienzeit des Bachelorstudiums? | 1 | 2 | 2 | 2 | 2 |
| 19 | In which semester does the practical semester take place? | 4 | 1 | 1 | 1 | 1 |
| 20 | Was passiert, wenn die Präsentation im Bachelorseminar ohne Erfolg bewertet wird? | 1 | 1 | 1 | 1 | 1 |
| 21 | How many members does the examination board have? | 1 | 1 | 1 | 1 | 1 |
| 22 | Wie viele Credits braucht man für den Eintritt in den zweiten Studienabschnitt? | 1 | 1 | 1 | 1 | 1 |
| 23 | What happens if Mathematics 1 and Programming 1 are not taken by the end of the second semester? | - | 1 | 1 | 1 | 1 |
| 24 | Wann wird das Thema der Bachelorarbeit frühestens ausgegeben? | 1 | 1 | 1 | 1 | 1 |
| 25 | Who supervises students during the internship? | 5 | - | - | - | - |
| 26 | Wie wird die Gesamtnote berechnet? | 1 | 1 | 1 | 1 | 1 |
| 27 | How many decimal places does the grade on the certificate have? | 1 | - | 5 | 5 | 5 |
| 28 | Wie heißt der Studiengang auf Englisch? | 1 | 1 | 1 | 1 | 1 |
| 29 | Is it possible to do the programme as a dual study? | 1 | 1 | 1 | 1 | 1 |
| 30 | Wann wird man aufgefordert, die Studienfachberatung aufzusuchen? | 1 | 1 | 1 | 1 | 1 |
| 31 | How many credits is the bachelor's thesis worth? | 1 | - | 5 | 4 | 4 |
| 32 | Wie viele Credits hat das Modul Programmieren 1? | 1 | 1 | 1 | 1 | 1 |
| 33 | What type of exam does Programming 1 have? | 1 | 3 | 3 | 3 | 3 |
| 34 | In welcher Sprache findet das Seminar statt? | 3 | 1 | 1 | 1 | 1 |
| 35 | What is the standard period of study? | 3 | 1 | 1 | 1 | 1 |
| 36 | Wie viele Vertiefungsmodule gibt es im dritten Studienabschnitt? | - | 5 | 5 | 5 | - |
| 37 | How many credits are earned in the first study section? | 5 | - | - | - | - |
| 38 | Wie viele Credits hat das Modul Physik? | 1 | - | 5 | 5 | 5 |
| 39 | How many credits does the Embedded Systems module have? | 3 | 3 | 3 | 3 | 3 |
| 40 | Was bedeutet die Abkürzung schrP? | - | - | - | - | - |