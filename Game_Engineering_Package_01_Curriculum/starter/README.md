# Course starter laboratory

Start with `day01_motion.py`. It uses only the Python standard library.
Read START_HERE.pdf before attempting the later C++ or hardware work.
These are original instructional examples, not a finished game engine.

## Python: macOS / Linux
Open a terminal **in this starter folder**, then run:

```sh
python3 --version
python3 day01_motion.py
python3 grid_game.py
python3 grid_game.py --replay SSSSDDDDDD
python3 -m unittest discover -v
```

## Python: Windows
Open PowerShell **in this starter folder**, then run:

```powershell
py -3 --version
py -3 day01_motion.py
py -3 grid_game.py
py -3 grid_game.py --replay SSSSDDDDDD
py -3 -m unittest discover -v
```

When the `py` launcher is not installed but `python --version` identifies
Python 3, use `python` in place of `py -3`. On macOS/Linux, use the verified
Python 3 command actually installed on the machine. No administrator command,
package installation, paid account or network access is required to RUN these files
once Python is installed. Install Python from its official distribution if needed.

Expected motion output:

```text
tick 1: x=1.50 units
tick 2: x=3.00 units
tick 3: x=4.50 units
tick 4: x=6.00 units
tick 5: x=7.50 units
```

`simulation.py` is a later reference for function contracts and validation.
`grid_game.py` uses classes and dataclasses taught after the first lessons.
You may play it on Day 1, but do not expect to understand every line yet.
The winning sample replay demonstrates reproducibility; find another route or
change the map after studying the rules. Do not treat supplied code as completed
coursework: labs require your own explanation, modifications and tests.

## C++: begin at Module 11, not on Day 1
Prerequisites: a C++20-capable compiler and CMake. From this starter folder:

```sh
cmake -S cpp -B cpp/build
cmake --build cpp/build --config Debug
ctest --test-dir cpp/build -C Debug --output-on-failure
```

Executable location depends on the CMake generator. Single-configuration systems
commonly use `cpp/build/motion_demo`; Visual Studio-style generators commonly
use `cpp/build/Debug/motion_demo.exe`.

The course package includes TESTED_ENVIRONMENT.md with the actual environment
used for the supplied examples. Windows/macOS command forms are supplied, but
execution tests here are limited to the recorded Linux container.

## Safe working habits
Keep experiments in their own directory and commit your own changes with Git.
Do not run unexplained administrative commands, disable protections or upload
private data to make an example work. The supplied programs do not contact a
server, delete files or require credentials.
