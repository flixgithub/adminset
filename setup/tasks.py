#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from subprocess import Popen, PIPE
from cmdb.models import Host
import sh, os
from config.views import get_dir
scripts_dir = get_dir("s_path")


@shared_task
def command(host, name):
    h = Host.objects.get(hostname=host)
    cmd = sh.ssh("root@"+h.ip, " "+name)
    data = str(cmd)
    return data


@shared_task
def script(host, name):
    h = Host.objects.get(hostname=host)
    sh.scp(scripts_dir+name, "admin@"+h.ip+":/tmp/"+name)
    file_suffix = os.path.splitext(name)[1]
    cmd = "ssh admin@" + h.ip + " " + '"sh /tmp/{}"'.format(name)
    if file_suffix == '.sh':
        cmd = "ssh admin@" + h.ip + " " + '"sh /tmp/{}"'.format(name)
    elif file_suffix == '.py':
        cmd = "ssh admin@" + h.ip + " " + '"python /tmp/{}"'.format(name)
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    data = p.communicate()
    return data

