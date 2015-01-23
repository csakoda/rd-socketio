import os

from socketio import socketio_manage
from socketio.server import SocketIOServer

from rdchat import ChatNamespace

public = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'public'))

homepage = 'test.html'

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
