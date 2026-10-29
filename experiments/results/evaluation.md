# Evaluation

44 questions (23 English, 21 German), 40 answerable and 4 not answerable from the documents. LLM: `qwen2.5:7b`, prompt v2, top-5 retrieval with re-ranking.

## Retrieval (answerable questions)

| search | hit@5 | 95 % CI | MRR | 95 % CI | hit@5 English | hit@5 German |
|---|---|---|---|---|---|---|
| vector | 0.90 | 0.80–0.97 | 0.73 | 0.60–0.84 | 0.81 | 1.00 |
| keyword | 0.70 | 0.55–0.82 | 0.55 | 0.41–0.68 | 0.62 | 0.79 |
| hybrid | 0.85 | 0.75–0.95 | 0.67 | 0.54–0.79 | 0.86 | 0.84 |
| hybrid + rerank | 0.90 | 0.80–0.97 | 0.76 | 0.63–0.86 | 0.86 | 0.95 |

## Answers (the app's default pipeline)

| metric | result |
|---|---|
| correct fact in answer (answerable) | 33/40 (82%) |
| answer cites a source (answerable) | 33/40 (82%) |
| answer in the question's language | 39/39 (100%) of answers with a detectable language |
| wrongly says "not in the documents" (answerable) | 5/40 (12%) |
| correctly declines (unanswerable) | 4/4 (100%) |
| latency per question | median 10.2 s, max 19.8 s |

## Where the wrong answers come from

| cause | questions |
|---|---|
| search missed the right page (not in top 5) | 3 |
| right page retrieved, but the answer is wrong | 4 |
| correct answer | 33 |

## Every answer

| # | lang | question | expected | answer | fact | cited | retrieval rank |
|---|---|---|---|---|---|---|---|
| 1 | en | How many ECTS credits do I need to complete the bachelor's degree? | 210 credits (§ 12 Abs. 2) | You need to achieve exactly 210 ECTS credits to complete the bachelor's degree [1]. | yes | yes | 1 |
| 2 | de | Wie viele Credits braucht man für den Bachelorabschluss? | genau 210 Credits (§ 12 Abs. 2) | Die Bachelorprüfung hat bestanden, wer genau 210 Credits erreicht hat. [1] | yes | yes | 1 |
| 3 | en | How long is the internship in the practical semester? | 18 weeks (§ 5 Abs. 1) | The internship in the practical semester lasts 18 weeks [1]. | yes | yes | 1 |
| 4 | de | Wie viele Wochen dauert das Praktikum im praktischen Studiensemester? | 18 Wochen (§ 5 Abs. 1) | Das Praktikum im praktischen Studiensemester dauert 18 Wochen [1]. | yes | yes | 1 |
| 5 | en | How many credits do I need before I am admitted to the internship? | at least 90 credits (§ 8 Abs. 3) | You need at least 90 credits before you are admitted to the internship [2]. | yes | yes | 1 |
| 6 | de | Welche Voraussetzung gilt für die Zulassung zum Praktikum? | mindestens 90 Credits (§ 8 Abs. 3) | Die Zulassung zum Praktikum (Modul Nr. 22.1 gemäß Anlage) setzt voraus, dass mindestens 90 Credits erzielt wurden. [1, 3] | yes | no | 1 |
| 7 | en | How long can I work on my bachelor's thesis? | max. 3 months, up to 5 months in special cases (§ 11 Abs. 4-5) | The Bearbeitungszeit for the written thesis can be up to five months, but this period can be reduced to three months if the thesis is started at least five mont… | yes | yes | 1 |
| 8 | de | Darf die Bachelorarbeit auf Englisch geschrieben werden? | ja, mit Genehmigung der Prüferin/des Prüfers (§ 11 Abs. 7) | Ja, die Bachelorarbeit darf mit Genehmigung der Prüferin oder des Prüfers in englischer Sprache abgefasst werden [1]. | yes | yes | 1 |
| 9 | en | How many hours of work does one ECTS credit correspond to? | 30 hours on average (§ 6 Abs. 1) | One ECTS credit corresponds to an average workload of 30 hours for presence and self-study. [1] | yes | yes | 1 |
| 10 | en | What level of English do applicants need? | B1 (CEFR) (§ 3 Abs. 3) | Applicants need to prove English proficiency at level B1 of the Common European Framework of Reference for Languages (GER) [1]. | yes | yes | 1 |
| 11 | de | Welche Deutschkenntnisse müssen ausländische Bewerber nachweisen? | DSH-1 oder gleichwertig (§ 3 Abs. 2) | Studienbewerberinnen und Studienbewerber, die ihre Hochschulzugangsberechtigung nicht an einer deutschsprachigen Bildungseinrichtung erworben haben, erbringen e… | yes | yes | 1 |
| 12 | en | Which exams must be taken by the end of the second semester? | Mathematik 1 and Programmieren 1 (§ 8 Abs. 1) | The exams for the modules "Mathematik 1" and "Programmieren 1" must be taken by the end of the second semester [1]. | yes | yes | 1 |
| 13 | de | Wie viele Credits braucht man für den Eintritt in den dritten Studienabschnitt? | mindestens 100 Credits, alle Prüfungen des 1. Abschnitts bestanden (§ 8 Abs. 4) | [2] In den dritten Studienabschnitt darf eintreten, wer alle Prüfungen des ersten Studienabschnitts bestanden hat und insgesamt mindestens 100 Credits erworben … | yes | yes | 1 |
| 14 | en | What academic degree do graduates receive? | Bachelor of Science (B.Sc.) (§ 13 Abs. 2) | Bachelor of Science, abbreviated B.Sc. [1] | yes | yes | 1 |
| 15 | en | How many credits is the practical semester worth? | 26 credits: internship 24 + seminar 2 (Anlage, Modul 22) | The practical semester is worth 26 credits [5]. | yes | yes | 5 |
| 16 | de | Wie lange ist die Amtszeit der Prüfungskommission? | drei Jahre (§ 10) | Die Amtszeit der Prüfungskommission beträgt drei Jahre [1]. | yes | yes | 1 |
| 17 | en | How many credits does the Databases module have? | 7 credits (Anlage, Modul 12) | The Databases module has 6 credits [5]. | no | yes | - |
| 18 | de | Was ist die Regelstudienzeit des Bachelorstudiums? | sieben Studiensemester (§ 4 Abs. 1) | Die Regelstudienzeit des Bachelorstudiums beträgt sieben Studiensemester. [2] | yes | yes | 2 |
| 19 | en | In which semester does the practical semester take place? | 5th semester (§ 4 Abs. 3, § 5 Abs. 1) | The practical semester takes place in the 5th semester [1, 2]. | yes | no | 1 |
| 20 | de | Was passiert, wenn die Präsentation im Bachelorseminar ohne Erfolg bewertet wird? | einmalige Wiederholung innerhalb eines Monats (§ 11 Abs. 6) | Die Präsentation im Bachelorseminar kann einmalig innerhalb eines Monats nach Bekanntgabe der Bewertung wiederholt werden. [1] | yes | yes | 1 |
| 21 | en | How many members does the examination board have? | chair plus two further members (§ 10 Abs. 1) | The examination board consists of three members [1]. | yes | yes | 1 |
| 22 | de | Wie viele Credits braucht man für den Eintritt in den zweiten Studienabschnitt? | mindestens 30 Credits im ersten Abschnitt (§ 8 Abs. 2) | [2] Zum Eintritt in den zweiten Studienabschnitt ist nur berechtigt, wer im ersten Studienabschnitt mindestens 30 Credits erzielt hat. | yes | yes | 1 |
| 23 | en | What happens if Mathematics 1 and Programming 1 are not taken by the end of the second semester? | they count as failed for the first time (§ 8 Abs. 1) | [1] If Mathematics 1 and Programming 1 are not taken by the end of the second semester, they are considered failed for the first time. | yes | yes | 1 |
| 24 | de | Wann wird das Thema der Bachelorarbeit frühestens ausgegeben? | frühestens im sechsten Studiensemester, nach bestandenem Praktikum (§ 11 Abs. 2) | Das Thema der Bachelorarbeit wird frühestens im sechsten Studiensemester ausgegeben [2]. | yes | yes | 1 |
| 25 | en | Who supervises students during the internship? | full-time teaching staff (§ 5 Abs. 2) | The documents do not contain this information. | no | no | - |
| 26 | de | Wie wird die Gesamtnote berechnet? | Endnoten aller Module × Notengewicht, summiert, geteilt durch die Summe der Notengewichte (§ 12 Abs. 3) | Die Gesamtnote wird berechnet, indem die Endnoten aller Module mit deren jeweiligem Notengewicht multipliziert, aufsummiert und durch die Summe aller Notengewic… | yes | yes | 1 |
| 27 | en | How many decimal places does the grade on the certificate have? | one decimal place (§ 13 Abs. 1) | The documents do not contain this information. | no | no | 5 |
| 28 | de | Wie heißt der Studiengang auf Englisch? | Computer Science / Technical Computer Science (§ 13 Abs. 3) | Die Studiengangbezeichnung lautet in der englischen Übersetzung „Computer Science“ [1]. Alternativ heißt der Studiengang „Technical Computer Science“ [2]. | yes | yes | 1 |
| 29 | en | Is it possible to do the programme as a dual study? | yes, with a contract with a company approved by the university (§ 3 Abs. 4) | Yes, it is possible for students to do the programme as a dual study. [2] | yes | yes | 1 |
| 30 | de | Wann wird man aufgefordert, die Studienfachberatung aufzusuchen? | unter 30 Credits am Ende des 2. Fachsemesters, vor einer zweiten Wiederholungsprüfung (§ 9) | Studierende werden aufgefordert, die Studienfachberatung aufzusuchen, wenn sie bis zum Ende des zweiten Fachsemesters noch keine 30 Credits erreicht haben [1]. … | yes | yes | 1 |
| 31 | en | How many credits is the bachelor's thesis worth? | 15 credits: thesis 12 + seminar 3 (Anlage, Modul 32) | The bachelor's thesis is worth 15 credits [4]. | yes | yes | 4 |
| 32 | de | Wie viele Credits hat das Modul Programmieren 1? | 8 Credits (Anlage, Modul 6) | Das Modul Programmieren 1 hat 8 Credits [1]. | yes | yes | 1 |
| 33 | en | What type of exam does Programming 1 have? | written exam, 90 minutes (Anlage, Modul 6) | The Programming 1 module has a written exam [3]. | no | yes | 3 |
| 34 | de | In welcher Sprache findet das Seminar statt? | Englisch (Anlage, Modul 21) | Unterrichts- und Prüfungssprache Englisch 1 [1]. | yes | yes | 1 |
| 35 | en | What is the standard period of study? | seven semesters, six theoretical and one practical (§ 4 Abs. 1) | The standard period of study is seven semesters [1]. | yes | yes | 1 |
| 36 | de | Wie viele Vertiefungsmodule gibt es im dritten Studienabschnitt? | sieben Vertiefungsmodule (Anlage, Module 23–29) | Die Dokumente enthalten dazu keine Angabe. | no | no | 5 |
| 37 | en | How many credits are earned in the first study section? | 60 credits (Anlage, Summe 1. Studienabschnitt) | The documents do not contain this information. | no | no | - |
| 38 | de | Wie viele Credits hat das Modul Physik? | 5 Credits (nur Technische Informatik, Anlage, Modul 3) | Die Dokumente enthalten dazu keine Angabe. | no | no | 5 |
| 39 | en | How many credits does the Embedded Systems module have? | 5 credits (Technische Informatik, Anlage, Modul 18) | The Embedded Systems module has 5 credits [3]. | yes | yes | 3 |
| 40 | de | Was bedeutet die Abkürzung schrP? | schriftliche Prüfung (Abkürzungsverzeichnis) | Die Abkürzung schrP steht für "Schriftliche Prüfung" [2]. | yes | yes | - |
| 41 | en | How much are the semester fees? | not in the regulations; the system should say it does not know | The documents do not contain this information. | declined | no | n/a |
| 42 | de | Wo befindet sich die Mensa? | not in the regulations; the system should say it does not know | Die Dokumente enthalten dazu keine Angabe. | declined | no | n/a |
| 43 | en | Can I do my internship abroad? | not in the regulations; the system should say it does not know | The documents do not contain this information. | declined | no | n/a |
| 44 | de | Wie viele Studierende werden pro Jahr zugelassen? | not in the regulations; the system should say it does not know | Die Dokumente enthalten dazu keine Angabe. | declined | no | n/a |