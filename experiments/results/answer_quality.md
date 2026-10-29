# Answer quality experiment

44 questions (40 answerable). One change per row; scoring as in eval/report.py.

| variant | model | prompt | re-rank | correct fact | cited | right language | wrongly declines | declines unanswerable | search misses | answer misses | median s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. baseline | llama3.2 | v1 | no | 19/40 (48%) | 27/40 (68%) | 13/25 (52%) | 7 | 3/4 | 6 | 15 | 3.6 |
| 2. prompt v2 | llama3.2 | v2 | no | 23/40 (57%) | 33/40 (82%) | 35/35 (100%) | 4 | 3/4 | 6 | 11 | 4.0 |
| 3. bigger model | qwen2.5:7b | v2 | no | 26/40 (65%) | 30/40 (75%) | 38/38 (100%) | 8 | 4/4 | 5 | 9 | 12.7 |
| 4. + re-ranking | qwen2.5:7b | v2 | yes | 31/40 (78%) | 31/40 (78%) | 38/38 (100%) | 7 | 4/4 | 7 | 2 | 9.6 |

## Correct fact per question

| # | question | 1. baseline | 2. prompt v2 | 3. bigger model | 4. + re-ranking |
|---|---|---|---|---|---|
| 1 | How many ECTS credits do I need to complete the bachelor's degree? | no | no | no | yes |
| 2 | Wie viele Credits braucht man für den Bachelorabschluss? | no | no | no | yes |
| 3 | How long is the internship in the practical semester? | no | no | no | yes |
| 4 | Wie viele Wochen dauert das Praktikum im praktischen Studiensemester? | yes | yes | yes | yes |
| 5 | How many credits do I need before I am admitted to the internship? | no | yes | yes | yes |
| 6 | Welche Voraussetzung gilt für die Zulassung zum Praktikum? | yes | yes | yes | yes |
| 7 | How long can I work on my bachelor's thesis? | no | no | no | yes |
| 8 | Darf die Bachelorarbeit auf Englisch geschrieben werden? | yes | yes | yes | yes |
| 9 | How many hours of work does one ECTS credit correspond to? | yes | yes | yes | yes |
| 10 | What level of English do applicants need? | no | yes | yes | yes |
| 11 | Welche Deutschkenntnisse müssen ausländische Bewerber nachweisen? | yes | yes | yes | yes |
| 12 | Which exams must be taken by the end of the second semester? | no | no | no | yes |
| 13 | Wie viele Credits braucht man für den Eintritt in den dritten Studienabschnitt? | yes | yes | yes | yes |
| 14 | What academic degree do graduates receive? | yes | yes | yes | yes |
| 15 | How many credits is the practical semester worth? | no | yes | yes | no |
| 16 | Wie lange ist die Amtszeit der Prüfungskommission? | yes | yes | yes | yes |
| 17 | How many credits does the Databases module have? | no | no | no | no |
| 18 | Was ist die Regelstudienzeit des Bachelorstudiums? | yes | yes | yes | yes |
| 19 | In which semester does the practical semester take place? | no | no | no | yes |
| 20 | Was passiert, wenn die Präsentation im Bachelorseminar ohne Erfolg bewertet wird? | yes | yes | yes | yes |
| 21 | How many members does the examination board have? | yes | yes | yes | yes |
| 22 | Wie viele Credits braucht man für den Eintritt in den zweiten Studienabschnitt? | yes | yes | yes | yes |
| 23 | What happens if Mathematics 1 and Programming 1 are not taken by the end of the second semester? | no | no | no | yes |
| 24 | Wann wird das Thema der Bachelorarbeit frühestens ausgegeben? | yes | yes | yes | yes |
| 25 | Who supervises students during the internship? | no | no | no | no |
| 26 | Wie wird die Gesamtnote berechnet? | yes | yes | yes | yes |
| 27 | How many decimal places does the grade on the certificate have? | no | no | yes | no |
| 28 | Wie heißt der Studiengang auf Englisch? | yes | yes | yes | yes |
| 29 | Is it possible to do the programme as a dual study? | yes | yes | yes | yes |
| 30 | Wann wird man aufgefordert, die Studienfachberatung aufzusuchen? | yes | yes | yes | yes |
| 31 | How many credits is the bachelor's thesis worth? | no | no | yes | no |
| 32 | Wie viele Credits hat das Modul Programmieren 1? | no | no | no | yes |
| 33 | What type of exam does Programming 1 have? | no | no | no | no |
| 34 | In welcher Sprache findet das Seminar statt? | yes | yes | yes | yes |
| 35 | What is the standard period of study? | yes | yes | yes | yes |
| 36 | Wie viele Vertiefungsmodule gibt es im dritten Studienabschnitt? | no | no | no | no |
| 37 | How many credits are earned in the first study section? | no | no | no | no |
| 38 | Wie viele Credits hat das Modul Physik? | no | no | no | no |
| 39 | How many credits does the Embedded Systems module have? | no | yes | yes | yes |
| 40 | Was bedeutet die Abkürzung schrP? | no | no | yes | yes |
| 41 | How much are the semester fees? | declined | declined | declined | declined |
| 42 | Wo befindet sich die Mensa? | declined | declined | declined | declined |
| 43 | Can I do my internship abroad? | answered | answered | declined | declined |
| 44 | Wie viele Studierende werden pro Jahr zugelassen? | declined | declined | declined | declined |

## Answers of the last variant

1. **How many ECTS credits do I need to complete the bachelor's degree?**  
   expected: 210 credits (§ 12 Abs. 2)  
   answer: 210 credits [1].
2. **Wie viele Credits braucht man für den Bachelorabschluss?**  
   expected: genau 210 Credits (§ 12 Abs. 2)  
   answer: Die Bachelorprüfung hat bestanden, wer genau 210 Credits erreicht hat [1].
3. **How long is the internship in the practical semester?**  
   expected: 18 weeks (§ 5 Abs. 1)  
   answer: The internship in the practical semester lasts 18 weeks [1].
4. **Wie viele Wochen dauert das Praktikum im praktischen Studiensemester?**  
   expected: 18 Wochen (§ 5 Abs. 1)  
   answer: Das Praktikum im praktischen Studiensemester dauert 18 Wochen [1].
5. **How many credits do I need before I am admitted to the internship?**  
   expected: at least 90 credits (§ 8 Abs. 3)  
   answer: You need at least 90 credits before you are admitted to the internship [2].
6. **Welche Voraussetzung gilt für die Zulassung zum Praktikum?**  
   expected: mindestens 90 Credits (§ 8 Abs. 3)  
   answer: Die Zulassung zum Praktikum (Modul Nr. 22.1 gemäß Anlage) setzt voraus, dass mindestens 90 Credits erzielt wurden. [1, 3]
7. **How long can I work on my bachelor's thesis?**  
   expected: max. 3 months, up to 5 months in special cases (§ 11 Abs. 4-5)  
   answer: The Bearbeitungszeit for the written elaboration of the bachelor's thesis should be appropriate for the topic and must not exceed three months when worked on continuously and exclusively. [1] The duration can be extended to five months if the thesis is handed out no later than five months before the end of a semester in which at least one further examination in the compulsory or elective area has to be taken, and an application is submitted to the chair of the examination board. [2]
8. **Darf die Bachelorarbeit auf Englisch geschrieben werden?**  
   expected: ja, mit Genehmigung der Prüferin/des Prüfers (§ 11 Abs. 7)  
   answer: Ja, die Bachelorarbeit darf mit Genehmigung der Prüferin oder des Prüfers in englischer Sprache abgefasst werden [1].
9. **How many hours of work does one ECTS credit correspond to?**  
   expected: 30 hours on average (§ 6 Abs. 1)  
   answer: One ECTS credit corresponds to an average workload of 30 hours for presence and self-study. [1]
10. **What level of English do applicants need?**  
   expected: B1 (CEFR) (§ 3 Abs. 3)  
   answer: Applicants need to prove English proficiency at level B1 of the Common European Framework of Reference for Languages (GER). [1]
11. **Welche Deutschkenntnisse müssen ausländische Bewerber nachweisen?**  
   expected: DSH-1 oder gleichwertig (§ 3 Abs. 2)  
   answer: Studienbewerberinnen und Studienbewerber, die ihre Hochschulzugangsberechtigung nicht an einer deutschsprachigen Bildungseinrichtung erworben haben, müssen einen Nachweis über Deutschkenntnisse auf dem Niveau der Deutschen Sprachprüfung für den Hochschulzugang ausländischer Studienbewerber (DSH) mit einem Gesamtergebnis von mindestens DSH-1 oder einem äquivalenten Sprachnachweis erbringen [2].
12. **Which exams must be taken by the end of the second semester?**  
   expected: Mathematik 1 and Programmieren 1 (§ 8 Abs. 1)  
   answer: The exams for the modules "Mathematik 1" and "Programmieren 1" must be taken by the end of the second semester [1].
13. **Wie viele Credits braucht man für den Eintritt in den dritten Studienabschnitt?**  
   expected: mindestens 100 Credits, alle Prüfungen des 1. Abschnitts bestanden (§ 8 Abs. 4)  
   answer: [2] In den dritten Studienabschnitt darf eintreten, wer alle Prüfungen des ersten Studienabschnitts bestanden hat und insgesamt mindestens 100 Credits erworben hat.
14. **What academic degree do graduates receive?**  
   expected: Bachelor of Science (B.Sc.) (§ 13 Abs. 2)  
   answer: Bachelor of Science, abbreviated B.Sc. [1]
15. **How many credits is the practical semester worth?**  
   expected: 26 credits: internship 24 + seminar 2 (Anlage, Modul 22)  
   answer: The practical semester is worth 90 credits [3].
16. **Wie lange ist die Amtszeit der Prüfungskommission?**  
   expected: drei Jahre (§ 10)  
   answer: Die Amtszeit der Prüfungskommission beträgt drei Jahre [1].
17. **How many credits does the Databases module have?**  
   expected: 7 credits (Anlage, Modul 12)  
   answer: The passages do not contain this information.
18. **Was ist die Regelstudienzeit des Bachelorstudiums?**  
   expected: sieben Studiensemester (§ 4 Abs. 1)  
   answer: Die Regelstudienzeit des Bachelorstudiums umfasst sieben Studiensemester, sechs theoretischen und einem praktischen Studiensemester [2].
19. **In which semester does the practical semester take place?**  
   expected: 5th semester (§ 4 Abs. 3, § 5 Abs. 1)  
   answer: The practical semester takes place in the 5th semester [1, 2].
20. **Was passiert, wenn die Präsentation im Bachelorseminar ohne Erfolg bewertet wird?**  
   expected: einmalige Wiederholung innerhalb eines Monats (§ 11 Abs. 6)  
   answer: Die Präsentation im Bachelorseminar kann einmalig innerhalb eines Monats nach Bekanntgabe der Bewertung wiederholt werden. [1]
21. **How many members does the examination board have?**  
   expected: chair plus two further members (§ 10 Abs. 1)  
   answer: The examination board consists of three members [1].
22. **Wie viele Credits braucht man für den Eintritt in den zweiten Studienabschnitt?**  
   expected: mindestens 30 Credits im ersten Abschnitt (§ 8 Abs. 2)  
   answer: [2] Zum Eintritt in den zweiten Studienabschnitt ist nur berechtigt, wer im ersten Studienabschnitt mindestens 30 Credits erzielt hat.
23. **What happens if Mathematics 1 and Programming 1 are not taken by the end of the second semester?**  
   expected: they count as failed for the first time (§ 8 Abs. 1)  
   answer: The Prüfungen in den Modulen „Mathematik 1“ und „Programmieren 1“ are considered erstmalig nicht bestanden if they are not completed by the end of the second semester [1].
24. **Wann wird das Thema der Bachelorarbeit frühestens ausgegeben?**  
   expected: frühestens im sechsten Studiensemester, nach bestandenem Praktikum (§ 11 Abs. 2)  
   answer: Das Thema der Bachelorarbeit wird frühestens im sechsten Studiensemester ausgegeben [2].
25. **Who supervises students during the internship?**  
   expected: full-time teaching staff (§ 5 Abs. 2)  
   answer: The documents do not contain this information.
26. **Wie wird die Gesamtnote berechnet?**  
   expected: Endnoten aller Module × Notengewicht, summiert, geteilt durch die Summe der Notengewichte (§ 12 Abs. 3)  
   answer: Die Gesamtnote wird berechnet, indem die Endnoten aller Module mit deren jeweiligem Notengewicht multipliziert, aufsummiert und durch die Summe aller Notengewichte dividiert. [1]
27. **How many decimal places does the grade on the certificate have?**  
   expected: one decimal place (§ 13 Abs. 1)  
   answer: The documents do not contain this information.
28. **Wie heißt der Studiengang auf Englisch?**  
   expected: Computer Science / Technical Computer Science (§ 13 Abs. 3)  
   answer: Die Studiengangbezeichnung lautet in der englischen Übersetzung „Computer Science“ [1]. Alternativ heißt der Studiengang „Technical Computer Science“ [2].
29. **Is it possible to do the programme as a dual study?**  
   expected: yes, with a contract with a company approved by the university (§ 3 Abs. 4)  
   answer: Yes, it is possible for students to do the programme as a dual study. [2]
30. **Wann wird man aufgefordert, die Studienfachberatung aufzusuchen?**  
   expected: unter 30 Credits am Ende des 2. Fachsemesters, vor einer zweiten Wiederholungsprüfung (§ 9)  
   answer: Studierende werden aufgefordert, die Studienfachberatung aufzusuchen, wenn sie bis zum Ende des zweiten Fachsemesters noch keine 30 Credits erreicht haben [1]. Vor der Teilnahme an einer zweiten Wiederholungsprüfung werden sie ebenfalls aufgefordert, dies zu tun [2, 5].
31. **How many credits is the bachelor's thesis worth?**  
   expected: 15 credits: thesis 12 + seminar 3 (Anlage, Modul 32)  
   answer: The documents do not contain this information.
32. **Wie viele Credits hat das Modul Programmieren 1?**  
   expected: 8 Credits (Anlage, Modul 6)  
   answer: Das Modul Programmieren 1 hat 8 Credits [4].
33. **What type of exam does Programming 1 have?**  
   expected: written exam, 90 minutes (Anlage, Modul 6)  
   answer: The Programming 1 module has a written exam [3].
34. **In welcher Sprache findet das Seminar statt?**  
   expected: Englisch (Anlage, Modul 21)  
   answer: Unterrichts- und Prüfungssprache Englisch 1 [1].
35. **What is the standard period of study?**  
   expected: seven semesters, six theoretical and one practical (§ 4 Abs. 1)  
   answer: The standard period of study is seven semesters, with six theoretical and one practical semester [1].
36. **Wie viele Vertiefungsmodule gibt es im dritten Studienabschnitt?**  
   expected: sieben Vertiefungsmodule (Anlage, Module 23–29)  
   answer: Die Dokumente enthalten dazu keine Angabe.
37. **How many credits are earned in the first study section?**  
   expected: 60 credits (Anlage, Summe 1. Studienabschnitt)  
   answer: The documents do not contain this information.
38. **Wie viele Credits hat das Modul Physik?**  
   expected: 5 Credits (nur Technische Informatik, Anlage, Modul 3)  
   answer: Die Dokumente enthalten dazu keine Angabe.
39. **How many credits does the Embedded Systems module have?**  
   expected: 5 credits (Technische Informatik, Anlage, Modul 18)  
   answer: The Embedded Systems module has 5 credits [3].
40. **Was bedeutet die Abkürzung schrP?**  
   expected: schriftliche Prüfung (Abkürzungsverzeichnis)  
   answer: Die Abkürzung schrP steht für "Schriftliche Prüfung" [2].
41. **How much are the semester fees?**  
   expected: not in the regulations; the system should say it does not know  
   answer: The documents do not contain this information.
42. **Wo befindet sich die Mensa?**  
   expected: not in the regulations; the system should say it does not know  
   answer: Die Dokumente enthalten dazu keine Angabe.
43. **Can I do my internship abroad?**  
   expected: not in the regulations; the system should say it does not know  
   answer: The documents do not contain this information.
44. **Wie viele Studierende werden pro Jahr zugelassen?**  
   expected: not in the regulations; the system should say it does not know  
   answer: Die Dokumente enthalten dazu keine Angabe.