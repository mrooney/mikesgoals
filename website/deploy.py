#!/usr/bin/env python
import os
import re
import subprocess

import psutil

from settings_deploy import SERVICES

class Service(object):
    def __init__(self, name, port=None, pidfile=None, cwd=None, before=None, after=None, start=None, restart=None, stop=None, context=None, daemonizes=True, templates=None, **kwargs):
        self.name = name
        self.port = port
        self.pidfile = pidfile
        self.cwd = cwd
        self.before_cmd = before or False
        self.after_cmd = after or False
        self.start_cmd = start
        self.restart_cmd = restart or False
        self.stop_cmd = stop or ["kill", "{pid}"]
        self.context = context or {}
        self.daemonizes = daemonizes
        self.templates = templates or []
        self.__dict__.update(kwargs)

    def get_default_context(self, withpid=True):
        context = {
            'project_dir': os.path.abspath(os.path.dirname(__file__)),
            'pid': self.get_pid() if withpid else None,
        }
        context.update(self.__dict__)
        context.update(self.context)
        return context
    
    def format(self, strng, *args, **kwargs):
        return strng.format(**self.get_default_context(*args, **kwargs))

    def check_pid(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    def get_pid(self):
        if self.port:
            return self.get_pid_from_port()
        elif self.pidfile:
            return self.get_pid_from_file()
        else:
            raise Exception("Please specify either port or pidfile for service: " % self.name)

    def get_pid_from_file(self):
        pid = None
        try:
            pid = int(open(self.format(self.pidfile, withpid=False)).read().strip())
        except IOError:
            pass

        # Make sure a process with this pid actually exists.
        if pid and self.check_pid(pid):
            return pid

    def get_pid_from_port(self):
        try:
            path = "/usr/bin:/usr/sbin"
            results = subprocess.check_output(["lsof", "-i", ":%i"%self.port], env={"PATH": path}).splitlines()[1:]
        except subprocess.CalledProcessError:
            return None
        procs = [int(re.findall("[\w-]+", r)[1]) for r in results if "(LISTEN)" in r]
        # Assume the oldest process is the parent/master process.
        parent = sorted(procs, key=lambda p: psutil.Process(p).create_time)[0]
        return parent

    def is_running(self):
        return bool(self.get_pid())

    def run(self, cmd, **kwargs):
        for template in self.templates:
            Template(template).render(self)

        subproc_cmd = [self.format(arg, **kwargs) for arg in cmd]

        print " ".join(subproc_cmd)
        if self.daemonizes:
            runner = subprocess.check_call
        else:
            runner = subprocess.Popen
        return runner(subproc_cmd, cwd=self.cwd)

    def before(self):
        if self.before_cmd is not False:
            self.run(self.before_cmd)

    def after(self):
        if self.after_cmd is not False:
            # pid is not available in after_cmd, as it may be in flux / racey.
            self.run(self.after_cmd, withpid=False)

    def start(self, quick=False):
        print "Starting %s:" % self.name,
        if not quick:
            self.before()
        self.run(self.start_cmd)
        if not quick:
            self.after()

    def restart(self, quick=False):
        if self.restart_cmd:
            print "Restarting %s:" % self.name,
            if not quick:
                self.before()
            self.run(self.restart_cmd)
            if not quick:
                self.after()
        else:
            print "Ignoring %s, not configured to restart" % self.name

    def stop(self):
        print "Stopping %s:" % self.name,
        self.run(self.stop_cmd)

class Template(object):
    def __init__(self, filename):
        if not filename.endswith(".template"):
            raise Exception("Template paths must end with .template")
        self.filename = filename

    def render(self, service):
        context = service.get_default_context(withpid=False)

        full_path = os.path.join(self.filename.format(**context))
        templated_path = os.path.splitext(full_path)[0]

        contents = open(full_path).read().decode("utf8")
        contents = contents.format(**context)
        open(templated_path, "w").write(contents.encode("utf8"))
        return templated_path

def deploy(services, stop=False, quick=False):
    for service in services:
        if stop:
            if service.is_running():
                service.stop()
        elif service.is_running():
            service.restart(quick)
        else:
            service.start(quick)

if __name__ == "__main__":
    import sys
    service_objs = []
    for name, conf in SERVICES.items():
        service_objs.append(Service(name, **conf))
    deploy(service_objs, stop="stop" in sys.argv, quick="--quick" in sys.argv)
