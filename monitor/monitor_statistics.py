#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from appconf.models import Product_Detail
from django.db.models import Q
from accounts.permission import permission_verify
from cmdb.models import RdsGroup, Rds
from aliyunsdkcore.client import AcsClient
from aliyunsdkrds.request.v20140815 import DescribeSlowLogsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import DescribeSlowLogRecordsRequest
import json
import time


TIME_SECTOR = (
            3600,
            3600*3,
            3600*5,
            86400,
            86400*3,
            86400*7,
)

ACCESS_KEY_ID = 'LTAIBnLJzdPjmcLh'
ACCESS_KEY_SECRET = 'DGHhHtkGBCkgAZcq90Z2UDzJoH87Qk'


@login_required()
@permission_verify()
def sync_rds_info(request):
    temp_name = "monitor/monitor-header.html"
    client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'cn-shanghai')
    rds_env = {'prd': 'Production', 'pp': 'Pre-production', 'qa': 'Quality Assurance', 'dev': 'Develop', 'others': 'Others'}
    if RdsGroup.objects.all().count() != 0:
        RdsGroup.objects.all().delete()
        for name, desc in rds_env.items():
            RdsGroup(name=name, desc=desc).save()
    else:
        for name, desc in rds_env.items():
            RdsGroup(name=name, desc=desc).save()

    req = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    req.set_PageSize(100)
    resp = json.loads(client.do_action_with_exception(req), encoding='utf-8')

    for db in resp.get('Items').get('DBInstance'):
        db_instance_id = db.get('DBInstanceId')
        db_instance_description = db.get('DBInstanceDescription')
        db_instance_type = db.get('DBInstanceType')
        db_instance_class = db.get('DBInstanceClass')
        zone_id = db.get('ZoneId')
        connection_mode = db.get('ConnectionMode')
        engine = db.get('Engine')
        engine_version = db.get('EngineVersion')

        rds_group = db_instance_description.split('-')[-1]
        if rds_group in rds_env:
            group = RdsGroup.objects.get(name=rds_group)

            Rds(db_instance_id=db_instance_id, db_instance_description=db_instance_description, db_instance_type=db_instance_type, db_instance_class=db_instance_class, zone_id=zone_id, connection_mode=connection_mode, engine=engine, engine_version=engine_version, rds_group=group).save()
        else:
            group = RdsGroup.objects.get(name='others')

            Rds(db_instance_id=db_instance_id, db_instance_description=db_instance_description, db_instance_type=db_instance_type, db_instance_class=db_instance_class, zone_id=zone_id, connection_mode=connection_mode, engine=engine, engine_version=engine_version, rds_group=group).save()

    return render(request, "monitor/rds_index.html", locals())


@login_required()
@permission_verify()
def rds_slow_sql(request, db_instance_id, timing):
    temp_name = "monitor/monitor-header.html"

    if db_instance_id is None:
        return HttpResponse("<h3>db_instance_id can not be None!</h3>",content_type="text/html")
    else:
        t = time.localtime(time.time() - TIME_SECTOR[int(timing)])
        start_time = time.strftime("%Y-%m-%dT%H:%MZ", t)
        end_time = time.strftime("%Y-%m-%dT%H:%MZ", time.localtime())

        # request = DescribeSlowLogsRequest.DescribeSlowLogsRequest()
        req = DescribeSlowLogRecordsRequest.DescribeSlowLogRecordsRequest()
        req.set_DBInstanceId(db_instance_id)
        req.set_StartTime(start_time)
        req.set_EndTime(end_time)

        client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'cn-shanghai')
        resp = json.loads(client.do_action_with_exception(req), encoding='utf-8')
        slow_sql_list = resp.get('Items').get('SQLSlowRecord')

    return render(request, "monitor/rds_slow_sql.html", locals())
