# Course fixtures

winning_replay.json: 20 commands, expected x=9,y=9,energy=7,turns=18,status=won.
last_energy_win.json: 25 commands, expected x=9,y=9,energy=0,turns=25,status=won.
valid_save.json: reference starting state.
truncated_save.json: intentionally invalid JSON for failed-load experiments.

Do not “repair” the malformed fixture and then claim the rejection case was tested.
