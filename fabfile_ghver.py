# from fabric.api import run
from fabric.api import env, prompt, execute, sudo, run
from fabric.contrib.project import rsync_project, upload_project
import boto.ec2
import time


env.hosts = ['localhost',]


# add an environmental setting
env.aws_region = 'us-west-2'


def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


def provision_instance(wait_for_running=True, timeout=60, interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't1.micro'
    key_name = 'pk-aws'
    security_group = 'ssh-access'
    image_id = 'ami-37501207'

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ]
    )
    new_instances = [i for i in reservations.instances if i.state == u'pending']
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()


def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if not choice in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def run_command_on_selected_server(command):
    select_instance()
    selected_hosts = [
        'ubuntu@' + env.active_instance.public_dns_name
    ]
    execute(command, hosts=selected_hosts)


# def write_nginxconf():
#     select_instance()
#     addr = env.active_instance.public_dns_name
#     nginx_list = []
#     nginx_list.append('server {')
#     nginx_list.append('    listen 80;')
#     nginx_list.append('    server_name ' + addr + ';')
#     nginx_list.append('    access_log  /var/log/nginx/test.log;\n')
#     nginx_list.append('    location /static/ {')
#     nginx_list.append('    \troot /var/www/photorize/;')
#     nginx_list.append('    \tautoindex off;')
#     nginx_list.append('    }\n')
#     nginx_list.append('    location / {')
#     nginx_list.append('    \tproxy_pass http://127.0.0.1:8000;')
#     nginx_list.append('    \tproxy_set_header Host $host;')
#     nginx_list.append('    \tproxy_set_header X-Real-IP $remote_addr;')
#     nginx_list.append('    \tproxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;')
#     nginx_list.append('    }')
#     nginx_list.append('}')
#     nginx_config = '\n'.join(nginx_list)
#     with open('server_config/simple_nginx_config', 'w') as outfile:
#             outfile.write(nginx_config)


def _sync_it():
    # addr = env.active_instance.public_dns_name
    # run("sed -i.bac 's/server_name/server_name " + addr + ";/' server_config/simple_nginx_config")
    rsync_project('/home/ubuntu/', 'server_config/iuvo.conf')
    rsync_project('/home/ubuntu/', 'server_config/iuvo.nginxconf')
    sudo('mv /home/ubuntu/iuvo.conf /etc/supervisor/conf.d/')
    sudo('mv /home/ubuntu/iuvo.nginxconf /etc/nginx/sites-available/')
    sudo('mkdir /etc/nginx/ssl')  # Not needed if this is > than first app on server.
    sudo('cd /etc/nginx/sites-enabled/ && ln -s ../sites-available/iuvo.nginxconf .')
    sudo('groupadd --system webapps') # Not needed if this is > than first app on server.
    sudo('useradd --system --gid webapps --shell /bin/bash --home /webapps/iuvo iuvo_user')
    sudo('mkdir -p /webapps/iuvo')
    sudo('mkdir /webapps/iuvo/logs')
    sudo('touch /webapps/iuvo/logs/gunicorn_supervisor.log')
    sudo('usermod -a -G users ubuntu') # Not needed if this is > than first app on server.
    sudo('chown -R iuvo_user:users /webapps/iuvo')
    sudo('chmod -R g+w /webapps/iuvo')
    rsync_project('/webapps/iuvo/', 'iuvo')
    rsync_project('/webapps/iuvo/iuvo/iuvo_app/', '/var/www/iuvo/static')
    rsync_project('/webapps/iuvo/', 'requirements.txt')
    sudo('cd /webapps/iuvo/ && virtualenv . && source bin/activate && pip install -r requirements.txt gunicorn setproctitle django-s3-folder-storage && deactivate')
    sudo('chown -R iuvo_user:users /webapps/iuvo')
    sudo('chmod -R g+w /webapps/iuvo')
    rsync_project('/webapps/iuvo/bin/', 'server_config/gunicorn_start.sh')
    sudo('chmod u+x /webapps/iuvo/bin/gunicorn_start.sh')
    sudo('chown iuvo_user:users /webapps/iuvo/bin/gunicorn_start.sh')
    sudo('chmod g+w /webapps/iuvo/bin/gunicorn_start.sh')
    sudo('psql -c "create user iuvo_user with password \'xxxx\';"', user='postgres')
    sudo('createdb --owner iuvo_user iuvodb', user='postgres')
    # similar ssh: ssh aws 'sudo -u photorizer /bin/bash -c "cd /webapps/photorize && . bin/activate && photorize/manage.py findstatic jquery-1.11.1.min.js --configuration=Prod && whoami && deactivate"'
    sudo('cd /webapps/iuvo && . bin/activate && iuvo/manage.py migrate && iuvo/manage.py collectstatic --configuration=Prod && deactivate', user='iuvo_user')
    sudo('cd /webapps/iuvo && . bin/activate && iuvo/manage.py createsuperuser --username admin --email xxxx@xxxx.com && deactivate', user='iuvo_user')
    # The following not needed if this is > than first app on server.
    sudo('cd /etc/nginx/ssl && openssl genrsa -des -out server.key 1024 && openssl req -new -key server.key -out server.csr && cp server.key server.key.org && openssl rsa -in server.key.org -out server.key && openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt')

def sync_it():
    run_command_on_selected_server(_sync_it)


def _install_dep():
    sudo('apt-get update')
    sudo('apt-get -y upgrade')
    sudo('apt-get -y install postgresql postgresql-contrib')
    sudo('apt-get -y install python-virtualenv')
    sudo('apt-get -y install python-all-dev libpq-dev')  # dependencies for psycopg2
    sudo('apt-get -y install nginx')
    sudo('apt-get -y install supervisor')
    sudo('apt-get -y install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk')


def install_dep():
    run_command_on_selected_server(_install_dep)


def _start_server():
    sudo('service nginx start')
    sudo('supervisorctl reread')
    sudo('supervisorctl update')


def start_server():
    run_command_on_selected_server(_start_server)


def deploy():
    provision_instance()
    time.sleep(20)
    install_dep()
    sync_it()
    start_server()
    get_info()


def get_info():
    select_instance()
    print(env.active_instance.public_dns_name)

def stop_instance(interval='2'):
    select_instance()
    instance = env.active_instance
    instance.stop()
    wait_val = int(interval)
    while instance.state != 'stopped':
        time.sleep(wait_val)
        print "Instance %s is stopping" % instance.id
        instance.update()
    print "Instance %s is stopped" % instance.id


def terminate_instance(interval='2'):
    select_instance(state='stopped')
    instance = env.active_instance
    instance.terminate()
    instance.update()
    print(instance.state)
    print "Instance %s is terminated" % instance.id
