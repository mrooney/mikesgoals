import os

class Service(object):
    def __init__(self, name, pidfile=None, port=None, start=None, restart=None, stop=None):
        self.name = name
        self.pidfile = pidfile
        self.port = port
        self.start_cmd = start
        self.restart_cmd = restart
        self.stop_cmd = stop

    def get_pid(self):
        try:
            return int(file(self.pidfile).read())
        except (IOError, OSError, ValueError):
            return None

    def check_pid(self):
        try:
            os.kill(self.get_pid(), 0)
        except OSError:
            return False
        else:
            return True

    def is_running(self):
        return self.get_pid() and self.check_pid()

    def start(self):
        print "Starting", self.name
        print self.start_cmd

    def restart(self):
        print "Restarting", self.name
        print self.restart_cmd

    def stop(self):
        print "Stopping", self.name
        print self.stop_cmd

def templated(filename):
    pass

services = {
    "nginx":
        {
            "pidfile": "./run/nginx.pid",
            "port": 54030,
            "start": ["nginx", "-c", templated("nginx.conf.template")],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
            "stop": ["kill", "{pid}"],
        },
    "gunicorn":
        {
            "pidfile": "./run/gunicorn.pid",
            "port": 54031,
            "start": ["gunicorn", "-D", "settings_gunicorn.py", "goals.wsgi:application"],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
            "stop": ["kill", "{pid}"],
        },
}

def deploy(services):
    for service in services:
        if service.is_running():
            service.restart()
        else:
            service.start()

def stop(services):
    for service in services:
        service.stop()

if __name__ == "__main__":
    import sys

    service_objs = []
    for name, conf in services.items():
        service_objs.append(Service(name, **conf))

    if len(sys.argv) > 1 and sys.argv[1] == "stop":
        stop(service_objs)
    else:
        deploy(service_objs)
