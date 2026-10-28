# Evaluation

44 questions (23 English, 21 German), 40 answerable and 4 not answerable from the documents. LLM: `llama3.2`, top-5 retrieval.

## Retrieval (answerable questions)

| search | hit@5 | 95 % CI | MRR | 95 % CI | hit@5 English | hit@5 German |
|---|---|---|---|---|---|---|
| vector | 0.90 | 0.80–0.97 | 0.73 | 0.60–0.84 | 0.81 | 1.00 |
| keyword | 0.70 | 0.55–0.82 | 0.55 | 0.41–0.68 | 0.62 | 0.79 |
| hybrid | 0.85 | 0.75–0.95 | 0.67 | 0.54–0.79 | 0.86 | 0.84 |

## Answers (hybrid search + LLM)

| metric | result |
|---|---|
| correct fact in answer (answerable) | 19/40 (48%) |
| answer cites a source (answerable) | 22/40 (55%) |
| answer in the question's language | 14/27 (52%) of answers with a detectable language |
| wrongly says "not in the documents" (answerable) | 7/40 (18%) |
| correctly declines (unanswerable) | 3/4 (75%) |
| latency per question | median 4.2 s, max 8.2 s |

## Where the wrong answers come from

| cause | questions |
|---|---|
| search missed the right page (not in top 5) | 6 |
| right page retrieved, but the answer is wrong | 15 |
| correct answer | 19 |

## Every answer

| # | lang | question | expected | answer | fact | cited | retrieval rank (hybrid) |
|---|---|---|---|---|---|---|---|
| 1 | en | How many ECTS credits do I need to complete the bachelor's degree? | 210 credits (§ 12 Abs. 2) | [3] (OTH_Informatik_SPO_2024.pdf, p. 4) | no | yes | - |
| 2 | de | Wie viele Credits braucht man für den Bachelorabschluss? | genau 210 Credits (§ 12 Abs. 2) | Mindestens 100 Credits. [4] | no | yes | - |
| 3 | en | How long is the internship in the practical semester? | 18 weeks (§ 5 Abs. 1) | Die Dauer des Praktikums im Praktischen Studiensemester beträgt 24 Stunden. | no | no | 3 |
| 4 | de | Wie viele Wochen dauert das Praktikum im praktischen Studiensemester? | 18 Wochen (§ 5 Abs. 1) | Das Praktikum im praktischen Studiensemester dauert 18 Wochen. [1] | yes | yes | 1 |
| 5 | en | How many credits do I need before I am admitted to the internship? | at least 90 credits (§ 8 Abs. 3) | [3] | no | yes | 1 |
| 6 | de | Welche Voraussetzung gilt für die Zulassung zum Praktikum? | mindestens 90 Credits (§ 8 Abs. 3) | Mindestens 90 Credits müssen erzielt worden sein. [3] | yes | yes | 2 |
| 7 | en | How long can I work on my bachelor's thesis? | max. 3 months, up to 5 months in special cases (§ 11 Abs. 4-5) | [2] Die Bearbeitungszeit kann bis zu fünf Monate umfassen, wenn die Bachelorarbeit spätestens fünf Monate vor dem Ende eines Fachsemesters ausgegeben wird, in d… | no | yes | 2 |
| 8 | de | Darf die Bachelorarbeit auf Englisch geschrieben werden? | ja, mit Genehmigung der Prüferin/des Prüfers (§ 11 Abs. 7) | Ja, die Bachelorarbeit darf mit Genehmigung der Prüferin oder des Prüfers in englischer Sprache abgefasst werden. [1] | yes | yes | 1 |
| 9 | en | How many hours of work does one ECTS credit correspond to? | 30 hours on average (§ 6 Abs. 1) | 30 Stunden [1][2][3] | yes | yes | 1 |
| 10 | en | What level of English do applicants need? | B1 (CEFR) (§ 3 Abs. 3) | [1] | no | yes | 1 |
| 11 | de | Welche Deutschkenntnisse müssen ausländische Bewerber nachweisen? | DSH-1 oder gleichwertig (§ 3 Abs. 2) | Mindestens DSH-1 oder ein äquivalenter Sprachnachweis. | yes | no | 1 |
| 12 | en | Which exams must be taken by the end of the second semester? | Mathematik 1 and Programmieren 1 (§ 8 Abs. 1) | Es gibt keine explizite Angabe in den bereitgestellten Passagen, welche Exams unabhängig vom Modul oder Semester zu belegen sind. | no | no | - |
| 13 | de | Wie viele Credits braucht man für den Eintritt in den dritten Studienabschnitt? | mindestens 100 Credits, alle Prüfungen des 1. Abschnitts bestanden (§ 8 Abs. 4) | Mindestens 100 Credits. | yes | no | 1 |
| 14 | en | What academic degree do graduates receive? | Bachelor of Science (B.Sc.) (§ 13 Abs. 2) | B.Sc. (Bachelor of Science) | yes | no | 1 |
| 15 | en | How many credits is the practical semester worth? | 26 credits: internship 24 + seminar 2 (Anlage, Modul 22) | [2] | no | yes | 2 |
| 16 | de | Wie lange ist die Amtszeit der Prüfungskommission? | drei Jahre (§ 10) | Die Amtszeit der Prüfungskommission beträgt drei Jahre. [1] | yes | yes | 1 |
| 17 | en | How many credits does the Databases module have? | 7 credits (Anlage, Modul 12) | Leider gibt es in den bereitgestellten Passagen keine Informationen über den Credits des Moduls "Databases". | no | no | 4 |
| 18 | de | Was ist die Regelstudienzeit des Bachelorstudiums? | sieben Studiensemester (§ 4 Abs. 1) | Sechs theoretische und ein praktischer Studiensemester. | yes | no | 1 |
| 19 | en | In which semester does the practical semester take place? | 5th semester (§ 4 Abs. 3, § 5 Abs. 1) | Das Praktikum findet im 4. Semester statt. | no | no | 4 |
| 20 | de | Was passiert, wenn die Präsentation im Bachelorseminar ohne Erfolg bewertet wird? | einmalige Wiederholung innerhalb eines Monats (§ 11 Abs. 6) | Wenn die Präsentation im Bachelorseminar ohne Erfolg bewertet wird, kann sie einmalig innerhalb von einem Monat nach Bekanntgabe der Bewertung wiederholt werden… | yes | no | 1 |
| 21 | en | How many members does the examination board have? | chair plus two further members (§ 10 Abs. 1) | Die Prüfungskommission besteht aus dem vorsitzenden Mitglied und zwei weiteren Mitgliedern, also insgesamt 3 Mitglieder. [1][5] | yes | yes | 1 |
| 22 | de | Wie viele Credits braucht man für den Eintritt in den zweiten Studienabschnitt? | mindestens 30 Credits im ersten Abschnitt (§ 8 Abs. 2) | 30 Credits. [2] | yes | yes | 1 |
| 23 | en | What happens if Mathematics 1 and Programming 1 are not taken by the end of the second semester? | they count as failed for the first time (§ 8 Abs. 1) | Es ist nicht klar, was passiert, wenn Mathematik 1 und Programmieren 1 nicht an der Endes des zweiten Semesters absolviert werden. | no | no | - |
| 24 | de | Wann wird das Thema der Bachelorarbeit frühestens ausgegeben? | frühestens im sechsten Studiensemester, nach bestandenem Praktikum (§ 11 Abs. 2) | Frühestens im sechsten Studiensemester. [2] | yes | yes | 1 |
| 25 | en | Who supervises students during the internship? | full-time teaching staff (§ 5 Abs. 2) | Es ist nicht in den bereitgestellten Passagen angegeben, wer die Studierenden während der Praktika überwacht. | no | no | 5 |
| 26 | de | Wie wird die Gesamtnote berechnet? | Endnoten aller Module × Notengewicht, summiert, geteilt durch die Summe der Notengewichte (§ 12 Abs. 3) | Die Gesamtnote wird durch Multiplikation der Endnoten aller Module mit deren jeweiligem Notengewicht, Aufsummierung und Division durch die Summe aller Notengewi… | yes | no | 1 |
| 27 | en | How many decimal places does the grade on the certificate have? | one decimal place (§ 13 Abs. 1) | [5] (2 Nachkommastellen) | no | yes | 1 |
| 28 | de | Wie heißt der Studiengang auf Englisch? | Computer Science / Technical Computer Science (§ 13 Abs. 3) | Computer Science [1] | yes | yes | 1 |
| 29 | en | Is it possible to do the programme as a dual study? | yes, with a contract with a company approved by the university (§ 3 Abs. 4) | Ja, es ist möglich, das Programm als dualer Studienabschnitt zu studieren. [4] | yes | yes | 1 |
| 30 | de | Wann wird man aufgefordert, die Studienfachberatung aufzusuchen? | unter 30 Credits am Ende des 2. Fachsemesters, vor einer zweiten Wiederholungsprüfung (§ 9) | Man wird aufgefordert, die Studienfachberatung aufzusuchen, wenn man bis zum Ende des zweiten Fachsemesters noch keine 30 Credits erreicht hat [1] oder wenn man… | yes | yes | 1 |
| 31 | en | How many credits is the bachelor's thesis worth? | 15 credits: thesis 12 + seminar 3 (Anlage, Modul 32) | [2] [4] [5] | no | yes | 1 |
| 32 | de | Wie viele Credits hat das Modul Programmieren 1? | 8 Credits (Anlage, Modul 6) | Leider kann ich nicht bestätigen, wie viele Credits das Modul "Programmieren 1" hat. | no | no | 1 |
| 33 | en | What type of exam does Programming 1 have? | written exam, 90 minutes (Anlage, Modul 6) | Übungsabgabe. | no | no | 1 |
| 34 | de | In welcher Sprache findet das Seminar statt? | Englisch (Anlage, Modul 21) | Die Seminarinformatik findet in der englischen Sprache statt. [3] | yes | yes | 3 |
| 35 | en | What is the standard period of study? | seven semesters, six theoretical and one practical (§ 4 Abs. 1) | Die Standardzeit für ein Studium beträgt 7 Studiensemester. | yes | no | 3 |
| 36 | de | Wie viele Vertiefungsmodule gibt es im dritten Studienabschnitt? | sieben Vertiefungsmodule (Anlage, Module 23–29) | Es ist nicht möglich, die Anzahl der Vertiefungsmodule im dritten Studienabschnitt genau zu bestimmen, da die genauen Informationen nicht in den bereitgestellte… | no | no | - |
| 37 | en | How many credits are earned in the first study section? | 60 credits (Anlage, Summe 1. Studienabschnitt) | Es ist nicht explizit angegeben, wie viele Credits im ersten Studienabschnitt erworben werden müssen, um in den zweiten Studienabschnitt zu gelangen. Es wird je… | no | yes | 5 |
| 38 | de | Wie viele Credits hat das Modul Physik? | 5 Credits (nur Technische Informatik, Anlage, Modul 3) | Keine Angaben. | no | no | 1 |
| 39 | en | How many credits does the Embedded Systems module have? | 5 credits (Technische Informatik, Anlage, Modul 18) | Die Embedded Systems-Modul hat 2 Credits. [3] | no | yes | 3 |
| 40 | de | Was bedeutet die Abkürzung schrP? | schriftliche Prüfung (Abkürzungsverzeichnis) | Die Abkürzung schrP bedeutet "Schriftpraxis" oder "Schriftprüfung". | no | no | - |
| 41 | en | How much are the semester fees? | not in the regulations; the system should say it does not know | Es gibt keine explizite Angabe über die Semestergebühren in den bereitgestellten Passagen. | declined | no | n/a |
| 42 | de | Wo befindet sich die Mensa? | not in the regulations; the system should say it does not know | Es gibt keine Informationen über die Lage der Mensa in den bereitgestellten Passagen. | declined | no | n/a |
| 43 | en | Can I do my internship abroad? | not in the regulations; the system should say it does not know | Ja, das ist möglich. [1] | answered anyway | yes | n/a |
| 44 | de | Wie viele Studierende werden pro Jahr zugelassen? | not in the regulations; the system should say it does not know | Es ist nicht explizit angegeben, wie viele Studierende pro Jahr zugelassen werden. | declined | no | n/a |