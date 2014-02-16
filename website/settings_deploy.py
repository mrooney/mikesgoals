SERVICES = {
    "nginx":
        {
            "port": 54030,
            "start": "nginx -c {project_dir}/nginx.conf",
            "restart": "kill -s SIGHUP {pid}",
            "templates": ["nginx.conf.template"],
        },
    "gunicorn":
        {
            "port": 31511,
            "before": "bash before_deploy.sh",
            "start": "gunicorn -D -c settings_gunicorn.py goals.wsgi:application",
            "after": "bash after_deploy.sh",
            "restart": "kill -s SIGHUP {pid}",
        },
    "redis":
        {
            "port": 15126,
            "start": "redis-server redis.conf",
        },
}

