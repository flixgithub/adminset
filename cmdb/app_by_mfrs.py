#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from appconf.models import Product_Detail
from django.db.models import Q
from accounts.permission import permission_verify
import json


@login_required()
@permission_verify()
def get_info_by_mfrs(request):
    if request.method == 'GET':
        mfrs_name = request.GET.get('mfrs')  # get manufacture name
        if not mfrs_name:
            mfrs_name = 'cloud'
        app_datails = cache.get('app_details')
        if app_datails is None:
            app_details = Product_Detail.objects.filter(Q(env__startswith=mfrs_name))
            cache.set('app_details', app_details, 60*60)
    temp_name = "cmdb/app_by_mfrs-header.html"
    results ={
        'temp_name': temp_name,
        'app_details': app_details,
    }
    return render(request, 'cmdb/app_by_mfrs.html', results)


@login_required()
@permission_verify()
def export_info(request):
    pass