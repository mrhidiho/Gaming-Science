# Run directly, or use python run_example.py LESSON_ID from the bundle root.
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathkit import fit_line, rmse
train_x, train_y = (1, 2, 3, 4), (3, 5, 7, 9)
slope, intercept = fit_line(train_x, train_y)
test_x, test_y = (5, 6), (11, 14)  # synthetic held-out observations
predicted = [slope*x + intercept for x in test_x]
print("fitted slope and intercept:", slope, intercept)
print("held-out predictions:", predicted)
print(f"held-out RMSE: {rmse(test_y, predicted):.6f}")
