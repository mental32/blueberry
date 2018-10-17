import os
import json
import contextlib

from .child import Child


class BlueberryState:
    __slots__ = ('app', 'connections')

    def __init__(self, app):
        self.app = app
        self._clear()

    def _clear(self):
        self.connections = set()

    @property
    def identity(self):
        return os.getpid()

    @contextlib.contextmanager
    def refrence(self, ws, ws_data):
        child = Child(ws, ws_data)

        self.connections.add(child)

        yield child

        if not self.app.running:
            return

        if child in self.connections:
            self.connections.remove(child)

            for other in self.connections:
                self.app.loop.create_task(other.send(json.dumps({'op': 0, 'd': child.id})))
