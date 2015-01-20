import os

from socketio import socketio_manage
from socketio.server import SocketIOServer

from socketio.namespace import BaseNamespace

from interface import CommInterface, CommPacket
from rdgame import GameServer

server = GameServer()

public = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'public'))

homepage = 'test.html'

class ChatNamespace(BaseNamespace):
    _registry = {}

    def initialize(self):
        self._registry[id(self)] = self
        self.emit('connect')
        self.nick = None

    def disconnect(self, *args, **kwargs):
        del self._registry[id(self)]
        super(ChatNamespace, self).disconnect(*args, **kwargs)

    def on_logout(self):
        if not self.nick:
            return
        self.nick = None

    def on_login(self, nick):
        if self.nick:
            return
        self.nick = nick
        packet = CommPacket(sent_by=id(self), server_command='login', 
            server_args={'name': self.nick})
        CommInterface.send_to_gameserver(packet)

    def on_chat(self, message):
        if self.nick:
            packet = CommPacket(sent_by=id(self), message=message)
            print('The web server has received user input of [%s]' % packet.message)
            CommInterface.send_to_gameserver(packet)
        else:
            self.emit('chat', dict(u='SYSTEM', m='You must first login'))

    def _broadcast(self, event, message):
        for s in self._registry.values():
            s.emit(event, message)

    @classmethod
    def accept_message(cls, packet):
        print('The web server has received a response from the server.')
        for key, value in cls._registry.iteritems():
            if key in packet.send_to:
                print('Message: %s' % packet.message)
                value.emit('chat', dict(u='SYSTEM', m=packet.message))

CommInterface.gameserver = server
CommInterface.webserver = ChatNamespace

def chat(environ, start_response):
    if environ['PATH_INFO'].startswith('/socket.io'):
        return socketio_manage(environ, { '/chat': ChatNamespace })
    else:
        return serve_file(environ, start_response)

def serve_file(environ, start_response):
    path = os.path.normpath(
        os.path.join(public, environ['PATH_INFO'].lstrip('/')))
    assert path.startswith(public), path
    if os.path.exists(path) and os.path.isfile(path):
        start_response('200 OK', [('Content-Type', 'text/html')])
        with open(path) as fp:
            while True:
                chunk = fp.read(4096)
                if not chunk: break
                yield chunk
    else:
        path = os.path.normpath(
            os.path.join(path, homepage))
        if os.path.exists(path) and os.path.isfile(path):
            start_response('200 OK', [('Content-Type', 'text/html')])
            with open(path) as fp:
                while True:
                    chunk = fp.read(4096)
                    if not chunk: break
                    yield chunk
        else:
            start_response('404 NOT FOUND', [])
            yield 'File not found'

sio_server = SocketIOServer(
    ('', 8080), chat, 
    policy_server=False)
sio_server.serve_forever()
