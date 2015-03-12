# Simple EventEmitter-like class
class Evented():

    def __init__(self):
        self._event_handlers = []

    # Adds a listener for an event
    def on(self, event, fn):
        self._event_handlers.append((event, fn))

    # Dispatches an event
    def emit(self, event, *args):
        for handler in self._event_handlers:
            if handler[0] == event:
                handler[1](*args)
