"""Run from any working directory: python path/to/this_file.py."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from labs.run import main
if __name__ == '__main__':
    main(['demo','39.1'])
