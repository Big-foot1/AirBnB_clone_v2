#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
from datetime import datetime

env.hosts = ['54.87.171.64', '52.3.255.208']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        arch_name = archive_path.split('/')[1]
        arch_name_nex = arch_name.split(".")[0]
        re_path = "/data/web_static/releases/" + arch_name_nex
        up_path = '/tmp/' + arch_name
        put(archive_path, up_path)
        run('mkdir -p ' + re_path)
        run('tar -xzf /tmp/{} -C {}/'.format(arch_name, re_path))
        run('rm {}'.format(up_path))
        mv = 'mv ' + re_path + '/web_static/* ' + re_path + '/'
        run(mv)
        run('rm -rf ' + re_path + '/web_static')
        run('rm -rf /data/web_static/current')
        run('ln -s ' + re_path + ' /data/web_static/current')
        return True
    except:
        return False
