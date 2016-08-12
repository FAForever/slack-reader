from .. import socketio


@socketio.on('join')
def join():
    print('joined')
