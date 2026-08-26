# QBReader-to-PPT

Generate PowerPoint decks from QBReader tossups.

Credit to Geoffrey Wu, Rohan Arni, Sky Hong, and other contributors to QBReader and their API wrapper module.

## Requirements

The requirements are as follows:

```PowerShell
python-pptx
pywin32
qbreader
requests
```

To easily install them, run the following:

```PowerShell
pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

The root `main.py` file is the primary launcher. The application code lives in `qbtppt/`.

The program will open a series of GUI popups that guide you through building a PowerPoint deck from QBReader questions.

## Question Source

The first popup lets you choose how questions should be selected:

- **Random questions**: generate a random packet using filters such as difficulty, year, category, and distribution.
- **Select existing packet**: choose an existing QBReader set from a searchable list, then select a packet from that set.

## Random Question Options

When using random questions, you can configure:

- **Difficulty**: choose one or more QBReader difficulty levels.
- **Year range**: select a minimum and maximum year. The default range is 2000-2026.
- **Distribution**:
  - **NAQT-distro**
  - **ACF-distro**
  - **Just trash**
  - **None**
- **Categories**: if no standard distribution is selected, you can manually choose categories.
- **Bonuses**: choose whether to include bonuses.

Standard Distributions:

NAQT (novice): [www.naqt.com/college/collegiate-novice-distribution.jsp](https://www.naqt.com/college/collegiate-novice-distribution.jsp)

ACF: [acf-quizbowl.com/writing/distribution](https://acf-quizbowl.com/writing/distribution/)

This program does not account for subcategories or 0.5/0.5 within distros, but may be updated to include them in the future.

If bonuses are included with a standard distribution, the bonus distribution matches the tossup distribution.

If no standard distribution is selected, the program uses 20 tossups and, if enabled, 20 bonuses.

## Bonuses

Bonuses can be included in the generated PowerPoint.

When bonuses are enabled, they are interspersed with tossups:

```text
Tossup 1
Tossup 1 Answer
Bonus 1
Bonus 1 Answer
Tossup 2
Tossup 2 Answer
Bonus 2
Bonus 2 Answer
...
```

## PowerPoint Output

The generated deck includes:

- A configuration slide showing the selected options.
- One slide per tossup.
- One answer slide per tossup.
- Optional bonus slides and bonus answer slides.
- Word-by-word reveal animations for question text when PowerPoint COM automation is available.

The file is saved as:

```text
output.pptx
```

## Animation Notes

Reveal animations are added through PowerPoint COM automation, so they require:

- Windows
- Microsoft PowerPoint installed
- `pywin32` (in the requirements)

If animations cannot be added, the PowerPoint will still be generated.

## Project Structure

```text
config/
  defaults.json          Project defaults and PowerPoint animation constants
qbtppt/
  api/                   Direct QBReader API client
  gui/                   Tkinter selector popups
  ppt/                   PowerPoint generation and COM animation
  text/                  Tossup text parsing helpers
  trivia/                Categories, difficulties, and standard distributions
  app.py                 Main orchestration
  models.py              Shared dataclasses
  settings.py            Config loading
main.py                  Primary launcher
```
