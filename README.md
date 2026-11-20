# Student Dropout Story — CS1710 final project

Team: Anh Nguyen, Karis Ka, Maggie Peng, Amaka Ihejirika (Harvard CS1710, Fall 2026).

Data exploration and storyboard work for our data story on student dropout risk.
Process book: https://docs.google.com/document/d/1yUBoKTumUW06p0g8fcB6EA3Qu_pfeiUeGBxGHq7538Q/edit

## Main message (Milestone 7)

Dropout is not fate: by the end of the first semester, a handful of visible warning signs
(grades, missed deadlines, attendance, work hours, money and stress) separate a 5% dropout
risk from a 95% one, so students and schools can act months before anyone actually leaves.

The full Milestone 7 write-up (per-member insights, team discussion, storyboard) is in
[docs/milestone7.md](docs/milestone7.md).

## Layout

- `data/student_dropout_risk_2026.csv` — 100,000 students, 33 attributes, no missing values, 32% dropout.
- `analysis/analyze.py` — answers the twelve team questions (grades, background, engagement, wellbeing).
- `analysis/extra.py` — the seven-flag warning-sign ladder and interaction tables behind the main message.
- `analysis/figs.py` — per-member figures and the main-message figure.
- `analysis/storyboard.py` — the four-column data storyboard image.
- `figures/milestone7/` — rendered PNGs used in the process book.

## Run

```bash
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
./venv/bin/python analysis/analyze.py
./venv/bin/python analysis/extra.py
./venv/bin/python analysis/figs.py
./venv/bin/python analysis/storyboard.py
```

Run from the repo root; the scripts use paths relative to it.
