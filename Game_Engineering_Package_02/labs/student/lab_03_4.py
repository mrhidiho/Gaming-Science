# Student exercise. Expected to fail checks until implemented.
TRANSITIONS = {('idle', 'move'): 'moving', ('moving', 'stop'): 'idle', ('idle', 'hit'): 'stunned', ('moving', 'hit'): 'stunned', ('stunned', 'recover'): 'idle'}

def transition(state, event):
    """Unknown state is an error; an unlisted event leaves a valid state alone."""
    raise NotImplementedError('Implement Lesson 03.4; see the lab workbook.')
