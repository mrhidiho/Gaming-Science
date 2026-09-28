# Start Here
## A first session for today

**Goal:** run a small program, predict its behavior and explain the difference between input, state and output. No game engine, graphics SDK, electronics kit or paid account is needed today. The learner's age, prior programming and mathematics experience were not supplied, so this starting path assumes no programming experience and permits acceleration by demonstrated competence.

Extract the complete course ZIP into a folder you can find again. Open `CURRICULUM.html` in a browser for searchable lessons, or use the PDFs in `volumes`. The browser edition stores no information on a server. Assigned external readings still require internet access; they are linked, not copied into the package.

| Time budget | Activity | Evidence to keep |
| --- | --- | --- |
| 0-15 minutes | Read Lesson 01.1 and trace its five movement commands on paper. | Your predicted positions. |
| 15-40 minutes | Follow the setup instructions below and run `day01_motion.py`. | The command, Python version and output. |
| 40-60 minutes | Explain every line using the walkthrough. | A short explanation in your own words. |
| 60-80 minutes | Change speed to 10, predict the output, then run. Restore it and change the timestep to 0.5. | Predictions, observations and differences. |
| 80-100 minutes | Complete the three questions after 01.1 and the three after 01.2 before reading the answer key. | Six answers, marked afterward. |
| 100-120 minutes | Write a journal entry and optionally play the grid game. | One question to investigate next session. |

These are session-planning estimates, not a deadline. Setup may take longer. Take breaks, stop at a working checkpoint and resume without treating slower progress as failure. Completing the reading and practical check matters more than matching the clock.

## Open a shell and find the starter folder

A **terminal** is the window; a **shell** is the command interpreter inside it. PowerShell is a common Windows shell. Terminal is a common macOS terminal application. Linux has several terminal applications. Python is a different program launched from that shell.

Open the extracted `starter` folder in a terminal. Some file managers and editors offer an “Open in Terminal” option. Otherwise type `cd ` followed by the quoted folder path and press Enter. The path must be the actual path on the learner's computer; do not copy a fictional username from an example.

On macOS/Linux, `pwd` shows the current folder and `ls` lists its files. In PowerShell, `Get-Location` and `Get-ChildItem` do the same. Confirm that `day01_motion.py` is listed before continuing.

On **macOS or Linux**, first check the interpreter, then run the file:

```sh
python3 --version
python3 day01_motion.py
```

On **Windows**, a common Python launcher command is:

```powershell
py -3 --version
py -3 day01_motion.py
```

When `py` is unavailable but `python --version` reports a supported Python 3 installation, use `python day01_motion.py`. Use one verified interpreter command consistently. Do not use Python 2. The supplied code was tested with Python 3.13.5; that is the tested environment, not a claim that this particular release is always the newest or the only usable release.

When Python is missing, use the official Python downloads and setup documentation, then reopen the terminal and repeat the version check. Official entry points: [Python downloads](https://www.python.org/downloads/) and [Python setup and usage](https://docs.python.org/3/using/index.html). On a managed computer, use the approved installation process rather than changing security settings. You can complete the paper trace while installation is arranged. [R04]

## The first program, explained

Open `starter/day01_motion.py` in a plain-text code editor. Save changes to that file, not to a word-processing document or a file ending in `.py.txt`.

```python
position_units = 0.0
speed_units_per_second = 6.0
timestep_seconds = 0.25

for tick in range(1, 6):
    position_units = position_units + speed_units_per_second * timestep_seconds
    print(f"tick {tick}: x={position_units:.2f} units")
```

`position_units = 0.0` creates the starting position. An assignment evaluates the right side and binds the result to the name on the left. It does not make an algebraic equation that must remain true forever.

`speed_units_per_second = 6.0` says the player travels six units during one second. `timestep_seconds = 0.25` makes each update represent one quarter of a second. The names carry units so the calculation can be checked.

`range(1, 6)` supplies 1, 2, 3, 4 and 5. The upper endpoint is excluded. The indented lines execute once for each value. The movement line adds `6.0 * 0.25`, or 1.5 units, to the previous position. The print line displays the current state; it does not move the player. The formatting `:.2f` displays two digits after the decimal point. It changes the text presentation, not the underlying movement rule. [R03, R04]

Expected output:

```text
tick 1: x=1.50 units
tick 2: x=3.00 units
tick 3: x=4.50 units
tick 4: x=6.00 units
tick 5: x=7.50 units
```

Before each change, write the five expected positions. With speed 10 and the original timestep, each update adds 2.5 units and the last position is 12.5. With the original speed 6 and timestep 0.5, each update adds 3 units and the last position is 15. Change one variable at a time so a disagreement has a clear cause.

## Common first-day problems

| Symptom | What to check |
| --- | --- |
| Command not found, or Python is not recognized | Confirm Python is installed through the approved route; reopen the shell; check the available launcher command. |
| Cannot open file | List the current directory. Confirm the exact filename and that the terminal is inside `starter`. |
| A `>>>` prompt is visible | That is the interactive Python prompt, not the ordinary shell. Enter `exit()` to return, then run the file command in the shell. |
| Indentation error | Preserve consistent indentation beneath the `for` line. Do not mix arbitrary tabs and spaces. |
| Syntax error | Read the indicated line and the preceding one. Check quotes, parentheses and the colon after `for`. |
| Program runs but changes do not appear | Save the edited file and confirm that the command runs that same file, not another copy. |

Never respond to a setup error by running an unexplained administrator command, deleting system folders, disabling protections or sharing passwords. The supplied starter programs need none of those actions.

## A playable reward and later test commands

After the motion exercise, run the tiny terminal game:

```sh
python3 grid_game.py
```

Use `py -3` instead of `python3` on Windows when that is the verified launcher. Move with W/A/S/D to reach G; Q exits. A wall or boundary blocks movement but still consumes a turn. The supplied game uses classes and dataclasses that are taught later; playing it today does not require understanding every implementation detail.

The following command replays a complete route:

```sh
python3 grid_game.py --replay SSSSDDDDDD
```

The demonstration reaches position (6,4) on turn 10. Find a different route after learning the rules. In Module 04, run the supplied automated tests and write additional tests of your own:

```sh
python3 -m unittest discover -v
```

The package's 23 Python tests and C++ motion-contract test passed in the recorded Linux environment. They validate the supplied starter, not the learner's future work and not every operating system. See `starter/TESTED_ENVIRONMENT.md` for the exact scope.

## A two-week starting rhythm

This is a sample at roughly 10-15 study hours per week, not a promise that every reading or lab will fit. Repeat a session when the practical check is incomplete. Do not skip a concept merely to keep the dates aligned.

| Session | Focus |
| --- | --- |
| Day 1 | Lessons 01.1-01.2, paper trace, motion program and six quiz questions. |
| Day 2 | Lesson 01.3: predict assignments before execution; repair a failed swap. |
| Day 3 | Lesson 01.4: units, frame intervals and an engineering journal. |
| Day 4 | Lesson 02.1: values, types and text-to-number conversion. |
| Day 5 | Review Module 01; explain the motion program without looking at notes. |
| Days 6-7 | Optional gentle practice, catch-up or rest. No new topic quota. |
| Day 8 | Lesson 02.2: conditions and boundary tests. |
| Day 9 | Lesson 02.3: loops, progress and invariants. |
| Day 10 | Lesson 02.4: functions, return values and input contracts. |
| Day 11 | Repair missed questions and add your own function test cases. |
| Day 12 | Start Module 02's small resource-gathering simulation. |
| Day 13 | Review the module project; demonstrate one unfamiliar change. |
| Day 14 | Catch-up, planning and rest before Module 03. |

Begin each later session with a five-minute recall exercise. End with the exact command that runs the current project, one unresolved question and the next smallest testable step. Use `templates/LAB_JOURNAL.md` rather than relying on memory.

## How to know a lesson is learned

Answer the three questions **before** opening the answer key. Award 0 for incorrect/missing, 1 for partly correct or unsupported and 2 for correct with a clear explanation. A suggested formative threshold is at least **5/6**, plus the lesson's practical pass condition and completed assigned study. A quiz score alone does not establish engineering competence.

For a missed question, identify the mistaken idea, solve a changed example and retest after a delay. Do not merely copy the answer. A reviewer should occasionally ask for an unfamiliar variation or a live code change. AI can explain or critique, but the learner must predict, test and defend the result independently.

Next: complete the two full lessons included on the following pages, then continue with Volume 1. `PROGRAM_GUIDE.pdf` contains placement, prerequisites, hour estimates, all ten checkpoint projects, graduate expectations and the resource directory. `ANSWER_KEY.pdf` is deliberately separate from the printable lessons.
