from socketio.namespace import BaseNamespace
from interface import CommPacket
from rdgame import GameServer

class ChatNamespace(BaseNamespace):
    _registry = {}

    def initialize(self):
        self._registry[id(self)] = self
        self.emit('connect')
        self.nick = None
        # our connection to the GameServer for this ChatNamespace session
        self.server = GameServer(self)

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
        self.server.send_message(packet)

    def on_chat(self, message):
        if self.nick:
            packet = CommPacket(sent_by=id(self), message=message)
            print('The web server has received user input of [%s]' % packet.message)
            self.server.send_message(packet)
        else:
            self.emit('chat', dict(u='SYSTEM', m='You must first login'))

    def _broadcast(self, event, message):
        for s in self._registry.values():
            s.emit(event, message)

    def send_message(self, packet):
        print('The web server has received a response from the server.')
        for key, value in ChatNamespace._registry.iteritems():
            if key in packet.send_to:
                print('Message: %s' % packet.message)
                value.emit('chat', dict(u='SYSTEM', m=packet.message))
