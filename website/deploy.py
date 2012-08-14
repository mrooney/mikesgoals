#!/usr/bin/env python
import os
import subprocess

class Service(object):
    def __init__(self, name, pidfile=None, port=None, start=None, restart=None, stop=None, context=None):
        self.name = name
        self.pidfile = os.path.abspath(pidfile)
        self.port = port
        self.start_cmd = start
        self.restart_cmd = restart or ["true"]
        self.stop_cmd = stop or ["kill", "{pid}"]
        self.context = context or {}

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

    def run(self, cmd):
        subproc_cmd = []
        for arg in cmd:
            if isinstance(arg, Template):
                arg = arg.render(self)
            else:
                arg = arg.format(pid=self.get_pid())
            subproc_cmd.append(arg)

        print " ".join(subproc_cmd)
        return subprocess.Popen(subproc_cmd)

    def start(self):
        print "Starting %s:" % self.name,
        self.run(self.start_cmd)

    def restart(self):
        print "Restarting %s:" % self.name,
        self.run(self.restart_cmd)

    def stop(self):
        print "Stopping %s:" % self.name,
        self.run(self.stop_cmd)

class Template(object):
    def __init__(self, filename):
        if not filename.endswith(".template"):
            raise Exception("Template paths must end with .template")
        self.filename = filename

    def render(self, service):
        project_dir = os.path.abspath(os.path.dirname(__file__))
        context = service.__dict__.copy()
        context['project_dir'] = project_dir
        context.update(service.context)

        full_path = os.path.join(project_dir, self.filename)
        templated_path = os.path.splitext(full_path)[0]

        contents = open(full_path).read().decode("utf8")
        contents = contents.format(**context)
        open(templated_path, "w").write(contents.encode("utf8"))
        return templated_path

services = {
    "nginx":
        {
            "pidfile": "./run/nginx.pid",
            "port": 54030,
            "start": ["nginx", "-c", Template("nginx.conf.template")],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
        },
    "gunicorn":
        {
            "pidfile": "./run/gunicorn.pid",
            "port": 31511,
            "start": ["gunicorn", "-D", "-c", "settings_gunicorn.py", "goals.wsgi:application"],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
        },
    "redis":
        {
            "pidfile": "./run/redis.pid",
            "port": 15126,
            "start": ["redis-server", "redis.conf"],
        },
}

def deploy(services, stop=False):
    for service in services:
        if stop:
            service.stop()
        elif service.is_running():
            service.restart()
        else:
            service.start()

if __name__ == "__main__":
    import sys

    service_objs = []
    for name, conf in services.items():
        service_objs.append(Service(name, **conf))

    deploy(service_objs, stop="stop" in sys.argv)
