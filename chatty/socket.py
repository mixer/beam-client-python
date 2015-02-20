from .evented import Evented
from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
import random
import json

# A ws4py websocket wrapped in an Evented class.
class EventedWebSocket(TornadoWebSocketClient, Evented):
    def __init__(self, *args, **kwargs):
        Evented.__init__(self)
        TornadoWebSocketClient.__init__(self, *args, **kwargs)

    def received_message(self, data):
        self.emit('message', str(data))

    def opened(self):
        self.emit('opened')

    def closed(self, code, reason=None):
        self.emit('closed', code, reason)


# Handles the Beam socket protocol. Ported directly from Js, not
# super Pythonic.
class Socket(Evented):

    def __init__(self, addresses):
        Evented.__init__(self)

        self.addressOffset = random.randint(0, len(addresses)-1)
        self.addresses = addresses
        self.call_id = 0

        self._connect()

    def _get_addresss(self):
        self.addressOffset += 1
        if self.addressOffset >= len(self.addresses):
            self.addressOffset = 0

        return self.addresses[self.addressOffset]

    def _connect(self):
        address = self._get_addresss() + '/ws'
        print('Connecting to %s' % address)

        self.ws = EventedWebSocket(address, protocols=['http-only', 'chat'])
        self.ws.connect()

        self.ws.on('opened', lambda *args: self.emit('opened', *args))
        self.ws.on('closed', self._on_close)
        self.ws.on('message', self._parsePacket)

    def _parsePacket(self, packet_str):
        # Todo: more advanced parsing here
        packet = json.loads(packet_str)
        self.emit('message', packet['data'])

    def _on_close(self, code, reason=None):
        print('Socket closed [Code %s] %s' % (code, reason))
        print('Reestablishing the socket in 1 second.')
        self.emit('closed', code, reason)

        ioloop.IOLoop.instance().call_later(1, self._connect)

    def send(self, type, *args, **kwargs):
        packet = {
            'type': type,
            'arguments': args,
            'id': self.call_id
        }

        packet.update(kwargs)
        print(packet)
        self.ws.send(json.dumps(packet))
        self.call_id += 1

