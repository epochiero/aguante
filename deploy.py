from contextlib import contextmanager
import os

import paramiko


class Task():

    OVERRIDES = {}

    def __init__(self, env):
        self.client = paramiko.SSHClient()
        self.client._policy = paramiko.WarningPolicy()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.env = env
        self.client_config = self.get_ssh_config_for(self.env)
        self.client.connect(**self.client_config)

    def get_ssh_config_for(self, name, ssh_config_file="~/.ssh/config"):
        ssh_config = paramiko.SSHConfig()
        user_config_file = os.path.expanduser(ssh_config_file)
        if os.path.exists(user_config_file):
            with open(user_config_file) as f:
                ssh_config.parse(f)

        user_config = ssh_config.lookup(self.env)
        return {'username': user_config['user'],
                'hostname': user_config['hostname'],
                'key_filename': user_config['identityfile'][0],
                'port': int(user_config['port'])
                }

    def execute(self, cmd):
        cmd = self.get_full_cmd(cmd)
        print("[%s] Executing: %s" %
              (self.client_config['hostname'], cmd))
        stdin, stdout, stderr = self.client.exec_command(cmd)
        output = ''.join(stdout.readlines())
        errput = ''.join(stderr.readlines())
        if output:
            print("[%s] %s" %
                  (self.client_config['hostname'], output))
        if errput:
            print("[%s] %s" %
                  (self.client_config['hostname'], errput))

    def get_full_cmd(self, cmd):
        full_cmd = ''
        exec_path = self.OVERRIDES.get('exec_path', None)
        virtualenv = self.OVERRIDES.get('virtualenv', None)
        if exec_path:
            full_cmd += "cd %s; " % (exec_path)
        if virtualenv:
            full_cmd += "source /home/aguante/.virtualenvs/%s/bin/activate; " % (
                virtualenv)
        return full_cmd + "/bin/bash -l -c '%s'" % (cmd)

    @contextmanager
    def cd(self, path):
        self.OVERRIDES['exec_path'] = path
        yield
        self.OVERRIDES.pop('exec_path')

    @contextmanager
    def activate_virtualenv(self, venv_name):
        self.OVERRIDES['virtualenv'] = venv_name
        yield
        self.OVERRIDES.pop('virtualenv')


def sudo(cmd, user=None):
    if user:
        return "sudo -u %s %s" % (user, cmd)
    return "sudo %s" % (cmd)


def deploy(env):
    task = Task(env)
    with task.cd('/home/aguante/aguante/aguante'):
        task.execute('git pull')
        with task.activate_virtualenv('aguante'):
            task.execute('pip install --upgrade -r requirements.txt')
            task.execute('python manage.py migrate')
            task.execute('python manage.py collectstatic --noinput')


def get_sytem_packages():
    package_list = ['git', 'python3-pip', 'rabbitmq-server', 'nginx',
                    'supervisor', 'libxml2-dev', 'libxslt-dev', 'python-dev',
                    'zlib1g-dev']
    return ' '.join(package_list)


def provision(env):
    task = Task(env)
    task.execute(sudo('aptitude update'))
    task.execute(sudo(
        'DEBIAN_FRONTEND=noninteractive aptitude install -y {}'.format(get_sytem_packages())))
    task.execute(sudo('pip3 install virtualenvwrapper'))
    task.execute('virtualenv ~/.virtualenvs/aguante/')

#provision('aguante')
deploy('aguante')
