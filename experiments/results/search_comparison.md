# Search comparison

20 questions, 136 chunks. hit@5 / MRR@5 use the top 5; found@20 = a correct page anywhere in the top 20.

| variant | hit@5 | MRR@5 | found@20 |
|---|---|---|---|
| vector | 0.85 | 0.77 | 0.95 |
| keyword (all words) | 0.60 | 0.50 | 0.75 |
| keyword (content words) | 0.75 | 0.50 | 0.85 |
| hybrid (all words) | 0.85 | 0.70 | 1.00 |
| hybrid (content words) | 0.85 | 0.65 | 1.00 |
| hybrid + dedupe | 0.85 | 0.65 | 1.00 |
| hybrid kw x0.5 | 0.85 | 0.67 | 1.00 |
| hybrid kw x0.25 | 0.80 | 0.67 | 1.00 |

## Rank of the first correct page (- = not in top 20)

| # | question | vector | keyword (all words) | keyword (content words) | hybrid (all words) | hybrid (content words) | hybrid + dedupe | hybrid kw x0.5 | hybrid kw x0.25 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | How many ECTS credits do I need to complete the bachelor's degree? | - | - | 3 | 15 | 12 | 12 | 14 | 16 |
| 2 | Wie viele Credits braucht man für den Bachelorabschluss? | 5 | 17 | 12 | 4 | 6 | 6 | 6 | 6 |
| 3 | How long is the internship in the practical semester? | 1 | - | 4 | 4 | 3 | 3 | 3 | 3 |
| 4 | Wie viele Wochen dauert das Praktikum im praktischen Studiensemester? | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 5 | How many credits do I need before I am admitted to the internship? | 1 | 3 | 3 | 1 | 1 | 1 | 1 | 1 |
| 6 | Welche Voraussetzung gilt für die Zulassung zum Praktikum? | 1 | 1 | 7 | 1 | 3 | 3 | 2 | 1 |
| 7 | How long can I work on my bachelor's thesis? | 1 | 8 | 3 | 6 | 3 | 3 | 2 | 2 |
| 8 | Darf die Bachelorarbeit auf Englisch geschrieben werden? | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 9 | How many hours of work does one ECTS credit correspond to? | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 10 | What level of English do applicants need? | 1 | - | - | 1 | 1 | 1 | 1 | 1 |
| 11 | Welche Deutschkenntnisse müssen ausländische Bewerber nachweisen? | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 |
| 12 | Which exams must be taken by the end of the second semester? | 4 | - | - | 10 | 15 | 14 | 11 | 7 |
| 13 | Wie viele Credits braucht man für den Eintritt in den dritten Studienabschnitt? | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 14 | What academic degree do graduates receive? | 1 | - | - | 1 | 1 | 1 | 1 | 1 |
| 15 | How many credits is the practical semester worth? | 6 | 1 | 3 | 1 | 2 | 2 | 2 | 3 |
| 16 | Wie lange ist die Amtszeit der Prüfungskommission? | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 17 | How many credits does the Databases module have? | 11 | 4 | 5 | 3 | 4 | 4 | 4 | 7 |
| 18 | Was ist die Regelstudienzeit des Bachelorstudiums? | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 19 | In which semester does the practical semester take place? | 1 | 8 | 5 | 4 | 5 | 4 | 4 | 4 |
| 20 | Was passiert, wenn die Präsentation im Bachelorseminar ohne Erfolg bewertet wird? | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

## Keyword noise: chunks matched by the keyword query

| # | content words used | chunks matched (all words) | chunks matched (content words) |
|---|---|---|---|
| 1 | ects, credits, need, complete, bachelor, degree | 33 of 136 | 49 of 136 |
| 2 | viele, credits, braucht, bachelorabschluss | 74 of 136 | 22 of 136 |
| 3 | long, internship, practical, semester | 64 of 136 | 8 of 136 |
| 4 | viele, wochen, dauert, praktikum, praktischen, studiensemester | 61 of 136 | 19 of 136 |
| 5 | credits, need, before, admitted, internship | 33 of 136 | 22 of 136 |
| 6 | voraussetzung, gilt, zulassung, praktikum | 94 of 136 | 20 of 136 |
| 7 | long, work, bachelor, thesis | 11 of 136 | 32 of 136 |
| 8 | darf, bachelorarbeit, englisch, geschrieben, werden | 97 of 136 | 70 of 136 |
| 9 | hours, work, one, ects, credit, correspond | 8 of 136 | 22 of 136 |
| 10 | level, english, applicants, need | 2 of 136 | 0 of 136 |
| 11 | deutschkenntnisse, müssen, ausländische, bewerber, nachweisen | 9 of 136 | 8 of 136 |
| 12 | exams, must, taken, end, second, semester | 6 of 136 | 12 of 136 |
| 13 | viele, credits, braucht, eintritt, dritten, studienabschnitt | 97 of 136 | 36 of 136 |
| 14 | academic, degree, graduates, receive | 0 of 136 | 0 of 136 |
| 15 | credits, practical, semester, worth | 24 of 136 | 28 of 136 |
| 16 | lange, amtszeit, prüfungskommission | 107 of 136 | 8 of 136 |
| 17 | credits, databases, module, have | 43 of 136 | 43 of 136 |
| 18 | regelstudienzeit, bachelorstudiums | 91 of 136 | 2 of 136 |
| 19 | semester, practical, take, place | 64 of 136 | 10 of 136 |
| 20 | passiert, präsentation, bachelorseminar, ohne, erfolg, bewertet | 98 of 136 | 18 of 136 |

## Where keyword search beats vector search

- Q1 *How many ECTS credits do I need to complete the bachelor's degree?*: keyword rank 3, vector rank - (terms: ects, credits, need, complete, bachelor, degree)
- Q15 *How many credits is the practical semester worth?*: keyword rank 3, vector rank 6 (terms: credits, practical, semester, worth)
- Q17 *How many credits does the Databases module have?*: keyword rank 5, vector rank 11 (terms: credits, databases, module, have)

## Where vector search beats keyword search

- Q2 *Wie viele Credits braucht man für den Bachelorabschluss?*: vector rank 5, keyword rank 12 (terms: viele, credits, braucht, bachelorabschluss)
- Q3 *How long is the internship in the practical semester?*: vector rank 1, keyword rank 4 (terms: long, internship, practical, semester)
- Q5 *How many credits do I need before I am admitted to the internship?*: vector rank 1, keyword rank 3 (terms: credits, need, before, admitted, internship)
- Q6 *Welche Voraussetzung gilt für die Zulassung zum Praktikum?*: vector rank 1, keyword rank 7 (terms: voraussetzung, gilt, zulassung, praktikum)
- Q7 *How long can I work on my bachelor's thesis?*: vector rank 1, keyword rank 3 (terms: long, work, bachelor, thesis)
- Q10 *What level of English do applicants need?*: vector rank 1, keyword rank - (terms: level, english, applicants, need)
- Q12 *Which exams must be taken by the end of the second semester?*: vector rank 4, keyword rank - (terms: exams, must, taken, end, second, semester)
- Q14 *What academic degree do graduates receive?*: vector rank 1, keyword rank - (terms: academic, degree, graduates, receive)
- Q19 *In which semester does the practical semester take place?*: vector rank 1, keyword rank 5 (terms: semester, practical, take, place)

## Questions still outside the top 5 (hybrid kw x0.5)

### Q1: How many ECTS credits do I need to complete the bachelor's degree?
Expected: 210 credits (§ 12 Abs. 2)  
Correct page rank: vector -, keyword 3, hybrid kw x0.5 14

Top 5 retrieved:
1. Informatik p.3: § 6 Module und Leistungsnachweise (1) Für die erbrachten Studienleistungen werden ECTS-Cre
2. TechnischeInformatik p.3: Soweit es sich um Module außerhalb des Curriculums des Studiengangs handelt, kann einer Be
3. Informatik p.4: (4) In den dritten Studienabschnitt darf eintreten, wer alle Prüfungen des ersten Studiena
4. TechnischeInformatik p.10: Elective Module 3) 5 4 1) 1) 1) 1) 1), 4) 2 32 Bachelorarbeit (Bachelor‘s Thesis) 15 32.1 
5. Informatik p.3: § 7 Studienplan (1) Die Fakultät Informatik und Mathematik erstellt zur Sicherstellung des

### Q2: Wie viele Credits braucht man für den Bachelorabschluss?
Expected: genau 210 Credits (§ 12 Abs. 2)  
Correct page rank: vector 5, keyword 12, hybrid kw x0.5 6

Top 5 retrieved:
1. Informatik p.4: (2) Zum Eintritt in den zweiten Studienabschnitt ist nur berechtigt, wer im ersten Studien
2. Informatik p.4: (4) In den dritten Studienabschnitt darf eintreten, wer alle Prüfungen des ersten Studiena
3. TechnischeInformatik p.4: (3) Die Zulassung zum Praktikum (Modul Nr. 22.1 gemäß Anlage) setzt voraus, dass mindesten
4. Informatik p.7: Anlage: Übersicht über die Module, Leistungsnachweise und Credits im Bachelorstudiengang I
5. TechnischeInformatik p.7: Anlage: Übersicht über die Module, Leistungsnachweise und Credits im Bachelorstudiengang T

### Q12: Which exams must be taken by the end of the second semester?
Expected: Mathematik 1 and Programmieren 1 (§ 8 Abs. 1)  
Correct page rank: vector 4, keyword -, hybrid kw x0.5 11

Top 5 retrieved:
1. Informatik p.9: studienbegleitender LN Zulassungsvoraussetzungen 21 Seminar Informatik (Seminar Computer S
2. Informatik p.3: (2) Die Pflicht- und Wahlpflichtmodule, ihre Semesterwochenstundenzahl, die Art der Lehrve
3. TechnischeInformatik p.9: studienbegleitender LN Zulassungsvoraussetzungen 22 Praktisches Studiensemester (Practical
4. TechnischeInformatik p.3: Studierende müssen unter ihnen gemäß dieser Studien- und Prüfungsordnung eine bestimmte Au
5. Informatik p.12: mit Übungen Ü Übung Pr Praktikum V Vorlesung S Seminar SUW seminaristischer Unterricht bei
