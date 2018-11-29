#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from monitor import system, manage, api, monitor_statistics

urlpatterns = [
    url(r'^system/$', system.index, name='monitor'),
    url(r'^db/$', system.rds_index, name='rds_sql'),
    url(r'^db/(?P<db_instance_id>.+)/(?P<timing>\d+)/$', monitor_statistics.rds_slow_sql, name='slow_sql'),
    url(r'^manage/del/all/$', manage.drop_sys_info, name='drop_all'),
    url(r'^system/host/tree/$', system.tree_node, name='host_tree'),
    url(r'^system/rds/tree/$', system.rds_tree_node, name='rds_tree'),
    url(r'^manage/del/range/(?P<timing>[0-9])/$', manage.del_monitor_data, name='del_monitor_data'),
    url(r'^manage/$', manage.index, name='monitor_manage'),
    url(r'^manage/sync/$', monitor_statistics.sync_rds_info, name='sync_rds_info'),
    url(r'^system/(?P<hostname>.+)/(?P<timing>\d+)/$', system.host_info, name='host_info'),
    url(r'^get/cpu/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_cpu, name='get_cpu'),
    url(r'^get/mem/(?P<hostname>.+)/(?P<timing>\d+)/$', system.get_mem, name='get_mem'),
    url(r'^get/disk/(?P<hostname>.+)/(?P<timing>\d+)/(?P<partition>\d+)/$', system.get_disk, name='get_disk'),
    url(r'^get/net/(?P<hostname>.+)/(?P<timing>\d+)/(?P<net_id>\d+)/$', system.get_net, name='get_net'),
    url(r'^received/sys/info/$', api.received_sys_info, name='received_sys_info'),
]
