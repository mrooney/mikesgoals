import atexit
import os

bind = "127.0.0.1:31511"
pidfile = "./run/gunicorn.pid"
errorlog = "./run/gunicorn.log"
workers = 1

def get_port_filename():
    pid = os.getpid()
    return os.path.join(os.path.dirname(pidfile), "%s.port" % pid)

def when_ready(server):
    host, port = server.LISTENER.sock.getsockname()
    port_filename = get_port_filename()
    with file(port_filename, 'w') as portfile:
        print >>portfile, port

    @atexit.register
    def remove_portfile():
        os.unlink(port_filename)
