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

## Existing Packet Mode

Instead of generating random questions, you can choose **Select existing packet** in the first popup.

This mode lets you use a specific packet that already exists in the QBReader database. After selecting this option:

1. The program loads the available QBReader set list.
2. A searchable GUI opens with the available sets.
3. You can type into the search bar to narrow the set list.
4. After choosing a set, you select which packet number to use.
5. The program loads that packet directly instead of querying for random tossups and bonuses.

In existing packet mode, the program skips the random-selection popups for difficulty, year range, distribution, and category selection. The tossups and bonuses come from the selected packet itself.

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

## Using the Slides

Each tossup slide is designed to reveal gradually during play. The reader can advance through the clue text while keeping the answer available privately in the speaker notes.

To advance the slide, let the animations play out to completion. You can preview the completed animation by examining the "next animation" window on the right of presenter view.
At the end of each animation (gated by sentence or power mark), hit the right arrow key or spacebar to begin the next animation.

Recommended use:

1. Start the slideshow in Presenter View.
2. Read or reveal the tossup text as normal.
3. When a player buzzes, hit the "1" key to stop the animations and check the speaker notes for the answer.
4. If the answer is correct, stop reading and move to the answer slide.
5. If the answer is incorrect, continue revealing the tossup. You can resume by hitting the ` key (below Escape).

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
