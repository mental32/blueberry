import asyncio

import websockets


class WebsocketServer:
    def __init__(self, host, port, state, loop=None):
        self.loop = loop or asyncio.get_event_loop()

        self._host = host
        self._port = port
        self._server = None
        self._closing = []

        self.state = state

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
        data = await ws.recv()

        # No valid introduction if data is None.
        if data is None:
            await ws.close()
            return

        with self.state.refrence(ws, data):
            await ws.send(state.hot_refrences)

            while self.running:
                # Check to close individual ws
                if ws in self._closing:
                    break

                data = await ws.recv()
                await asyncio.sleep(0)
