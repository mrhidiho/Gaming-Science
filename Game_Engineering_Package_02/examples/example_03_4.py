# Worked demonstration for Lesson 03.4.
TRANSITIONS = {
    ("idle", "move"): "moving",
    ("moving", "stop"): "idle",
    ("idle", "hit"): "stunned",
    ("moving", "hit"): "stunned",
    ("stunned", "recover"): "idle",
}

class Controller:
    def __init__(self):
        self.state = "idle"

    def on_event(self, event):
        self.state = TRANSITIONS.get((self.state, event), self.state)

controller = Controller()
for event in ("move", "hit", "move", "recover"):
    controller.on_event(event)
    print(event, "->", controller.state)
