import asyncio
import json

import websockets


class WebsocketServer:
    def __init__(self, host, port, state, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.state = state

        self._host = host
        self._port = port
        self._server = None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    async def start(self):
        self._server = server = await websockets.serve(self.ws_handler, self._host, self._port, loop=self.loop)
        return server

    async def ws_handler(self, ws, path):
        if not self.state.app.running:
            return

        data = json.loads(await ws.recv())

        if set(data.keys()) != {'http'} or not isinstance(data['http'], str):
            return await ws.close()

        with self.state.refrence(ws, data) as child:
            while self.state.app.running:
                data = await child.recv()
                await asyncio.sleep(0)
