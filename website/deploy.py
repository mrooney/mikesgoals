#!/usr/bin/env python
import os
import re
import subprocess

from settings_deploy import SERVICES

class Service(object):
    def __init__(self, name, port=None, cwd=None, start=None, restart=None, stop=None, context=None, daemonizes=True, templates=None):
        self.name = name
        self.port = port
        self.cwd = cwd
        self.start_cmd = start
        self.restart_cmd = restart or False
        self.stop_cmd = stop or ["kill", "{pid}"]
        self.context = context or {}
        self.daemonizes = daemonizes
        self.templates = templates or []

    def get_default_context(self):
        context = {
            'project_dir': os.path.abspath(os.path.dirname(__file__)),
            'pid': self.get_pid(),
        }
        context.update(self.__dict__)
        context.update(self.context)
        return context

    def get_pid(self):
        try:
            results = subprocess.check_output(["/usr/sbin/lsof", "-i", ":%i"%self.port]).splitlines()[1:]
        except subprocess.CalledProcessError:
            return None
        procs = [int(re.findall("\w+", r)[1]) for r in results if "(LISTEN)" in r]
        parent = sorted(procs)[0]
        return parent

    def is_running(self):
        return bool(self.get_pid())

    def run(self, cmd):
        for template in self.templates:
            Template(template).render(self)

        subproc_cmd = []
        for arg in cmd:
            arg = arg.format(**self.get_default_context())
            subproc_cmd.append(arg)

        print " ".join(subproc_cmd)
        if self.daemonizes:
            runner = subprocess.check_call
        else:
            runner = subprocess.Popen
        return runner(subproc_cmd, cwd=self.cwd)

    def start(self):
        print "Starting %s:" % self.name,
        print self.run(self.start_cmd)

    def restart(self):
        if self.restart_cmd:
            print "Restarting %s:" % self.name,
            print self.run(self.restart_cmd)
        else:
            print "Ignoring %s, not configured to restart" % self.name

    def stop(self):
        print "Stopping %s:" % self.name,
        print self.run(self.stop_cmd)

class Template(object):
    def __init__(self, filename):
        if not filename.endswith(".template"):
            raise Exception("Template paths must end with .template")
        self.filename = filename

    def render(self, service):
        context = service.get_default_context()

        full_path = os.path.join(context['project_dir'], self.filename)
        templated_path = os.path.splitext(full_path)[0]

        contents = open(full_path).read().decode("utf8")
        contents = contents.format(**context)
        open(templated_path, "w").write(contents.encode("utf8"))
        return templated_path

def deploy(services, stop=False):
    for service in services:
        if stop:
            if service.is_running():
                service.stop()
        elif service.is_running():
            service.restart()
        else:
            service.start()

if __name__ == "__main__":
    import sys
    service_objs = []
    for name, conf in SERVICES.items():
        service_objs.append(Service(name, **conf))
    deploy(service_objs, stop="stop" in sys.argv)
