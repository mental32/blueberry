import os
import contextlib


class BlueberryState:
    def __init__(self):
        self._clear()

    def _clear(self):
        self.connections = set()

    @property
    def identity(self):
        return os.getpid()

    @contextlib.contextmanager
    def refrence(self, ws, ws_data):
        self.connections.add(ws)

        yield

        if ws in self.connections:
            self.connections.remove(ws)
