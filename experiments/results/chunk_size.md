# Chunk size experiment

Configurations are chunk size / overlap in characters. "raw" = PDF text without cleanup; all other rows use clean_text() (page headers, sentence numbers and line-break hyphens removed).

20 questions in English and German, top-5 retrieval. A hit = a correct page among the top 5 results.

| size / overlap | chunks | avg chars | vector hit@5 | vector MRR | hybrid hit@5 | hybrid MRR | ingest s |
|---|---|---|---|---|---|---|---|
| 800 / 120 raw | 72 | 599 | 0.80 | 0.77 | 0.85 | 0.70 | 7.2 |
| 400 / 60 | 136 | 302 | 0.85 | 0.77 | 0.90 | 0.69 | 3.3 |
| 800 / 0 | 69 | 584 | 0.85 | 0.73 | 0.80 | 0.62 | 4.4 |
| 800 / 120 | 71 | 599 | 0.80 | 0.70 | 0.80 | 0.62 | 4.0 |
| 1200 / 180 | 44 | 959 | 0.85 | 0.70 | 0.75 | 0.64 | 3.5 |

## Rank of the first correct page per question (hybrid; - = not in top results)

| # | question | 800 / 120 raw | 400 / 60 | 800 / 0 | 800 / 120 | 1200 / 180 |
|---|---|---|---|---|---|---|
| 1 | How many ECTS credits do I need to complete the bachelor's degree? | - | - | - | - | - |
| 2 | Wie viele Credits braucht man für den Bachelorabschluss? | - | 5 | 3 | - | 5 |
| 3 | How long is the internship in the practical semester? | 1 | 4 | 4 | 4 | - |
| 4 | Wie viele Wochen dauert das Praktikum im praktischen Studiensemester? | 1 | 1 | 1 | 1 | 1 |
| 5 | How many credits do I need before I am admitted to the internship? | 2 | 2 | - | 4 | 3 |
| 6 | Welche Voraussetzung gilt für die Zulassung zum Praktikum? | 1 | 1 | 1 | 1 | 1 |
| 7 | How long can I work on my bachelor's thesis? | 3 | 3 | 4 | 4 | 4 |
| 8 | Darf die Bachelorarbeit auf Englisch geschrieben werden? | 1 | 1 | 1 | 1 | 1 |
| 9 | How many hours of work does one ECTS credit correspond to? | 1 | 1 | 1 | 1 | 1 |
| 10 | What level of English do applicants need? | 1 | 1 | 3 | 3 | - |
| 11 | Welche Deutschkenntnisse müssen ausländische Bewerber nachweisen? | 1 | 1 | 1 | 1 | 1 |
| 12 | Which exams must be taken by the end of the second semester? | - | - | - | - | - |
| 13 | Wie viele Credits braucht man für den Eintritt in den dritten Studienabschnitt? | 1 | 1 | 1 | 1 | 1 |
| 14 | What academic degree do graduates receive? | 1 | 1 | 1 | 1 | 1 |
| 15 | How many credits is the practical semester worth? | 2 | 1 | 1 | 1 | 1 |
| 16 | Wie lange ist die Amtszeit der Prüfungskommission? | 1 | 1 | 1 | 1 | 1 |
| 17 | How many credits does the Databases module have? | 4 | 3 | 3 | 4 | 1 |
| 18 | Was ist die Regelstudienzeit des Bachelorstudiums? | 1 | 1 | 1 | 1 | 1 |
| 19 | In which semester does the practical semester take place? | 2 | 4 | - | - | - |
| 20 | Was passiert, wenn die Präsentation im Bachelorseminar ohne Erfolg bewertet wird? | 1 | 1 | 1 | 1 | 1 |

## End-to-end answers (hybrid search + LLM)

### How many ECTS credits do I need to complete the bachelor's degree?
Expected: 210 credits (§ 12 Abs. 2)

- **800 / 120 raw** (8.0 s): Es ist nicht direkt im bereitgestellten Text zu finden, wie viele ECTS-Credits insgesamt für das Bachelorstudium erforderlich sind. Es wird jedoch erwähnt, dass "Ein Credit entspricht im Durchschnitt einer Arbeitsbelastung für Präsenz- und Selbststudium von 30 Stunden" [5].  
  sources: OTH_Informatik p.7, OTH_TechnischeInformatik p.10, OTH_TechnischeInformatik p.7, OTH_TechnischeInformatik p.3, OTH_Informatik p.3
- **400 / 60** (3.4 s): [4] (mindestens 100 Credits)  
  sources: OTH_TechnischeInformatik p.3, OTH_Informatik p.3, OTH_Informatik p.4, OTH_Informatik p.4, OTH_TechnischeInformatik p.10
- **800 / 0** (7.7 s): Es gibt keine explizite Angabe in den bereitgestellten Passagen, wie viele ECTS-Credits insgesamt für die Absolvierung des Bachelorstudiengangs benötigt werden.  
  sources: OTH_Informatik p.3, OTH_TechnischeInformatik p.7, OTH_Informatik p.7, OTH_TechnischeInformatik p.3, OTH_Informatik p.3
- **800 / 120** (4.4 s): Es ist nicht direkt im angegebenen Text zu finden, wie viele ECTS-Credits insgesamt für die Bachelor-Ausbildung benötigt werden müssen.  
  sources: OTH_Informatik p.7, OTH_TechnischeInformatik p.7, OTH_TechnischeInformatik p.10, OTH_TechnischeInformatik p.3, OTH_Informatik p.3
- **1200 / 180** (14.2 s): [4] (OTH_TechnischeInformatik_SPO_2024.pdf, p. 3) [4]  
  sources: OTH_TechnischeInformatik p.7, OTH_Informatik p.7, OTH_TechnischeInformatik p.10, OTH_TechnischeInformatik p.3, OTH_Informatik p.11

### How long is the internship in the practical semester?
Expected: 18 weeks (§ 5 Abs. 1)

- **800 / 120 raw** (7.7 s): Die Dauer des Praktikums im Praktischen Studiensemester beträgt 24 Wochen.  
  sources: OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.9, OTH_Informatik p.9, OTH_TechnischeInformatik p.2, OTH_Informatik p.11
- **400 / 60** (4.9 s): Die Internschaft im Praktischen Studiensemester dauert 18 Wochen. [4]  
  sources: OTH_Informatik p.9, OTH_TechnischeInformatik p.9, OTH_Informatik p.11, OTH_Informatik p.3, OTH_Informatik p.5
- **800 / 0** (9.1 s): Die Dauer des Praktikums im Praktischen Studiensemester beträgt 18 Wochen.  
  sources: OTH_Informatik p.9, OTH_TechnischeInformatik p.9, OTH_Informatik p.11, OTH_Informatik p.3, OTH_TechnischeInformatik p.2
- **800 / 120** (5.8 s): Die Dauer des Praktikums im Praktischen Studiensemester beträgt 18 Wochen.  
  sources: OTH_Informatik p.9, OTH_TechnischeInformatik p.9, OTH_Informatik p.11, OTH_TechnischeInformatik p.3, OTH_Informatik p.3
- **1200 / 180** (11.7 s): [2] (OTH_TechnischeInformatik_SPO_2024.pdf, p. 9)  
  sources: OTH_Informatik p.9, OTH_TechnischeInformatik p.9, OTH_Informatik p.11, OTH_Informatik p.4, OTH_TechnischeInformatik p.4

### How many credits do I need before I am admitted to the internship?
Expected: at least 90 credits (§ 8 Abs. 3)

- **800 / 120 raw** (9.2 s): [3] (OTH_TechnischeInformatik_SPO_2024.pdf, p. 7) und [4] (OTH_TechnischeInformatik_SPO_2024.pdf, p. 10)  Um in den Praktikum (Modul Nr. 22.1 gemäß Anlage) eingeschrieben zu werden, müssen mindestens 90 Credits erzielt werden.  
  sources: OTH_Informatik p.7, OTH_TechnischeInformatik p.4, OTH_TechnischeInformatik p.7, OTH_TechnischeInformatik p.10, OTH_Informatik p.4
- **400 / 60** (3.8 s): [3]  
  sources: OTH_Informatik p.7, OTH_TechnischeInformatik p.4, OTH_Informatik p.4, OTH_Informatik p.4, OTH_TechnischeInformatik p.7
- **800 / 0** (7.4 s): Es gibt keine explizite Angabe in den bereitgestellten Passagen darüber, wie viele Credits erforderlich sind, um in das Internat (Praktikum) aufgenommen zu werden.  
  sources: OTH_Informatik p.7, OTH_TechnischeInformatik p.7, OTH_TechnischeInformatik p.10, OTH_Informatik p.10, OTH_Informatik p.9
- **800 / 120** (5.8 s): Du musst mindestens 90 Credits erzielt haben, bevor du für das Praktikum zugelassen wirst.  
  sources: OTH_Informatik p.7, OTH_TechnischeInformatik p.7, OTH_Informatik p.10, OTH_TechnischeInformatik p.4, OTH_Informatik p.11
- **1200 / 180** (15.2 s): [3] (OTH_Informatik_SPO_2024.pdf, p. 3) Die Zulassung zum Praktikum (Modul Nr. 22.1 gemäß Anlage) setzt voraus, dass mindestens 90 Credits erzielt wurden.  
  sources: OTH_Informatik p.7, OTH_TechnischeInformatik p.7, OTH_Informatik p.4, OTH_TechnischeInformatik p.4, OTH_Informatik p.9

### How many hours of work does one ECTS credit correspond to?
Expected: 30 hours on average (§ 6 Abs. 1)

- **800 / 120 raw** (5.4 s): [1][2][4]  
  sources: OTH_Informatik p.3, OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.3, OTH_Informatik p.3
- **400 / 60** (3.7 s): 30 Stunden [1][4]  
  sources: OTH_Informatik p.3, OTH_Informatik p.3, OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.3
- **800 / 0** (6.1 s): [1]  
  sources: OTH_TechnischeInformatik p.3, OTH_Informatik p.3, OTH_Informatik p.3, OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.7
- **800 / 120** (5.6 s): [1]  
  sources: OTH_Informatik p.3, OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.3, OTH_Informatik p.3
- **1200 / 180** (10.1 s): [1]  
  sources: OTH_TechnischeInformatik p.3, OTH_Informatik p.3, OTH_TechnischeInformatik p.3, OTH_Informatik p.3, OTH_TechnischeInformatik p.7

### How many credits is the practical semester worth?
Expected: 26 credits: internship 24 + seminar 2 (Anlage, Modul 22)

- **800 / 120 raw** (8.2 s): [2] (OTH_Informatik_SPO_2024.pdf, p. 9)  
  sources: OTH_TechnischeInformatik p.4, OTH_Informatik p.9, OTH_TechnischeInformatik p.9, OTH_Informatik p.3, OTH_Informatik p.4
- **400 / 60** (3.8 s): Es ist nicht explizit angegeben, wie viele Credits der Praktische Studiensemester (Practical Semester) ist.  
  sources: OTH_Informatik p.9, OTH_TechnischeInformatik p.9, OTH_TechnischeInformatik p.4, OTH_Informatik p.4, OTH_TechnischeInformatik p.3
- **800 / 0** (6.0 s): [2] (OTH_TechnischeInformatik_SPO_2024.pdf, p. 9)  
  sources: OTH_Informatik p.9, OTH_TechnischeInformatik p.9, OTH_Informatik p.4, OTH_TechnischeInformatik p.3, OTH_TechnischeInformatik p.4
- **800 / 120** (6.2 s): [2] (OTH_TechnischeInformatik_SPO_2024.pdf, p. 9)  
  sources: OTH_Informatik p.9, OTH_TechnischeInformatik p.9, OTH_TechnischeInformatik p.4, OTH_Informatik p.4, OTH_Informatik p.3
- **1200 / 180** (11.9 s): [1]  
  sources: OTH_TechnischeInformatik p.9, OTH_Informatik p.9, OTH_Informatik p.4, OTH_Informatik p.3, OTH_TechnischeInformatik p.4

## How the chunks of OTH_Informatik_SPO_2024.pdf page 3 look

### 800 / 120 raw: 4 chunks on this page
> Seite 3 von 12 (4) 1Im dritten Studienabschnitt vertiefen die Studierenden ihre Kenntnisse durch die Wahl - pflicht- und Vertiefungsmodule. 2Dieser Studienabschnitt beinhaltet auch die Anfertigung der Bachelorarbeit im 7. Studiensemester. (5) Für Studierende, die in der alternativen Form „duales Stu…
>
> 2Die Studierenden werden im Praktikum durch hauptamtliche Lehrpersonen betreut. § 6 Module und Leistungsnachweise (1) 1Für die erbrachten Studienleistungen werden ECTS-Credits2) vergeben. 2Ein Credit entspricht im Durchschnitt einer Arbeitsbelastung für Präsenz- und Selbststudium von 30 Stunden. (2)…
>
> (3) Alle Module sind entweder Pflichtmodule, Wahlpflichtmodule oder Wahlmodule. 1. Pflichtmodule sind die Module des Studiengangs, die für alle Studierenden verbindlich sind. 2. 1Wahlpflichtmodule sind die Module, die alternativ angeboten werden. 2Studierende müssen unter ihnen gemäß dieser Studien …
>

### 400 / 60: 8 chunks on this page
> (4) Im dritten Studienabschnitt vertiefen die Studierenden ihre Kenntnisse durch die Wahlpflicht- und Vertiefungsmodule. Dieser Studienabschnitt beinhaltet auch die Anfertigung der Bachelorarbeit im 7. Studiensemester. (5) Für Studierende, die in der alternativen Form „duales Studium“ studieren, gel…
>
> § 5 Praktisches Studiensemester (1) Das praktische Studiensemester findet im 5. Studiensemester statt. Es beinhaltet ein Praktikum im Umfang von 18 Wochen (Modul 22.1) sowie Lehrveranstaltung Nr. 22.2 gemäß Anlage. (2) Die Ableistung des Praktikums stellt eine Prüfungsleistung dar. Die Studierenden …
>
> § 6 Module und Leistungsnachweise (1) Für die erbrachten Studienleistungen werden ECTS-Credits2) vergeben. Ein Credit entspricht im Durchschnitt einer Arbeitsbelastung für Präsenz- und Selbststudium von 30 Stunden.
>

### 800 / 0: 4 chunks on this page
> (4) Im dritten Studienabschnitt vertiefen die Studierenden ihre Kenntnisse durch die Wahlpflicht- und Vertiefungsmodule. Dieser Studienabschnitt beinhaltet auch die Anfertigung der Bachelorarbeit im 7. Studiensemester. (5) Für Studierende, die in der alternativen Form „duales Studium“ studieren, gel…
>
> § 6 Module und Leistungsnachweise (1) Für die erbrachten Studienleistungen werden ECTS-Credits2) vergeben. Ein Credit entspricht im Durchschnitt einer Arbeitsbelastung für Präsenz- und Selbststudium von 30 Stunden. (2) Die Pflicht- und Wahlpflichtmodule, ihre Semesterwochenstundenzahl, die Art der L…
>
> Wahlpflichtmodule sind die Module, die alternativ angeboten werden. Studierende müssen unter ihnen gemäß dieser Studien - und Prüfungsordnung eine bestimmte Auswahl treffen. Der Fakultätsrat legt vor Beginn des Semesters fest, welche Mo dule zur Wahl durch die Studierenden zugelassen werden. Einzelh…
>

### 800 / 120: 4 chunks on this page
> (4) Im dritten Studienabschnitt vertiefen die Studierenden ihre Kenntnisse durch die Wahlpflicht- und Vertiefungsmodule. Dieser Studienabschnitt beinhaltet auch die Anfertigung der Bachelorarbeit im 7. Studiensemester. (5) Für Studierende, die in der alternativen Form „duales Studium“ studieren, gel…
>
> Die Studierenden werden im Praktikum durch hauptamtliche Lehrpersonen betreut. § 6 Module und Leistungsnachweise (1) Für die erbrachten Studienleistungen werden ECTS-Credits2) vergeben. Ein Credit entspricht im Durchschnitt einer Arbeitsbelastung für Präsenz- und Selbststudium von 30 Stunden. (2) Di…
>
> (3) Alle Module sind entweder Pflichtmodule, Wahlpflichtmodule oder Wahlmodule. 1. Pflichtmodule sind die Module des Studiengangs, die für alle Studierenden verbindlich sind. 2. Wahlpflichtmodule sind die Module, die alternativ angeboten werden. Studierende müssen unter ihnen gemäß dieser Studien - …
>

### 1200 / 180: 3 chunks on this page
> (4) Im dritten Studienabschnitt vertiefen die Studierenden ihre Kenntnisse durch die Wahlpflicht- und Vertiefungsmodule. Dieser Studienabschnitt beinhaltet auch die Anfertigung der Bachelorarbeit im 7. Studiensemester. (5) Für Studierende, die in der alternativen Form „duales Studium“ studieren, gel…
>
> Ein Credit entspricht im Durchschnitt einer Arbeitsbelastung für Präsenz- und Selbststudium von 30 Stunden. (2) Die Pflicht- und Wahlpflichtmodule, ihre Semesterwochenstundenzahl, die Art der Lehrveranstaltungen, die Prüfungen und studienbegleitenden Leistungsnachweise sowie die Credits sind in der …
>
> Die gewählten Module werden wie Pflichtmodule behandelt. 3. Wahlmodule sind Module, die für die Erreichung des Studienziels nicht verbindlich vorgeschrieben sind. Sie können von den Studierenden aus dem Studienangebot der Hochschule zusätzlich gewählt werden. Soweit es sich um Module außerhalb des C…
>
