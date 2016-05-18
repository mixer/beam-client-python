class Evented():
    """Simple EventEmitter-like class."""

    def __init__(self):
        self._event_handlers = []

    def on(self, event, function):
        """Adds a listener for an event."""
        self._event_handlers.append((event, function))

    def emit(self, event, *args):
        """Dispatches an event."""
        for handler in self._event_handlers:
            if handler[0] == event:
                handler[1](*args)
