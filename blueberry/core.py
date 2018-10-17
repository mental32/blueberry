import io
import os
import sys
import asyncio
import pathlib
import threading
import importlib
from contextlib import redirect_stdout

import flask
import websockets

from blueberry import _blueberries

from . import utils
from .state import BlueberryState
from .utils import timelog, check_inet_connectivity
from .server import WebsocketServer

_LIB_PATH = pathlib.Path(__file__).parents[0]

_SITE_STATIC = _LIB_PATH.joinpath('site_static').absolute()
_SITE_TEMPLATE = _LIB_PATH.joinpath('site_templates').absolute()

del _LIB_PATH


class BlueberryThread(threading.Thread):
    def __init__(self, loop, target):
        self._loop = loop
        self.__target = target

        super().__init__()
        self.daemon = True
        self.start()

    def run(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self.__target())
        self._loop.run_forever()


class Blueberry:
    def __init__(self, parent_addr, port):
        _blueberries[os.getpid()] = self

        self.state = BlueberryState(self)
        self.stdout = utils._timelog_stdout = sys.stdout

        if parent_addr is None:
            self._parent = None

        elif '::' not in parent_addr:
            self._parent_port = 3722
            self._parent = parent_addr

        else:
            self._parent, self._parent_port = parent_addr.split('::')

        self._running = False

        self._port = port
        self.__build_ws_delay = True

        self._ws_client_thread = BlueberryThread(asyncio.new_event_loop(), self.__build_ws)
        self._flask_app = app = flask.Flask(__name__, static_folder=_SITE_STATIC, template_folder=_SITE_TEMPLATE)

        module = importlib.import_module('blueberry.site')
        app.register_blueprint(module.public)
        app.register_blueprint(module.private)

    @property
    def running(self):
        return self._running

    async def __client_ws(self, loop):
        self._ws = ws = await websockets.connect('ws://{0}:{1}'.format(self._parent, self._parent_port - 1))

        await ws.send({'http': 'http://{0}:{1}'.format(utils.get_local_addr(), self._port)})

        while self._running:
            await ws.recv()

    async def __build_ws(self):
        loop = asyncio.get_event_loop()

        # sleep until we're allowed to execute
        while self.__build_ws_delay:
            await asyncio.sleep(0.1)

        try:
            if self._parent is not None:
                loop.create_task(self.__client_ws(loop))
        except OSError as e:
            print(e)
            self._running = False
            self.__build_ws_delay = True
            return

        self._ws_server = ws_server = WebsocketServer('0.0.0.0', self._port - 1, self.state, loop=loop)
        await ws_server.start()

        timelog('Running WS Server on ws://{0}:{1}'.format(utils.get_local_addr(), ws_server.port))

        self.__build_ws_delay = True

    def run(self):
        self._running = True

        timelog('Starting blueberry application... (PID: {0})'.format(self.state.identity))

        if self._parent is None:
            timelog('Warning! No parent node specified.')

        timelog('Blueberry avaliable at: {addr} (http://{addr}:{port})'.format(addr=utils.get_local_addr(), port=self._port))

        if not check_inet_connectivity():
            return timelog('No internet access detected!')

        self.__build_ws_delay = False
        while not self.__build_ws_delay:
            continue

        if not self._running:
            return

        with redirect_stdout(io.StringIO()):
            self._flask_app.run('0.0.0.0', self._port, debug=False)
