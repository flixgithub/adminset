#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import Product, Product_Detail
from forms import ProductForm, Product_Detail_Form
from django.db.models import Q
from accounts.permission import permission_verify
import json
import io


@login_required()
@permission_verify()
def product_list(request):
    # temp_name = "appconf/appconf-header.html"
    # all_product = Product.objects.all()
    # results = {
    #    'temp_name': temp_name,
    #    'all_product':  all_product,
    # }
    # return render(request, 'appconf/product_list.html', results)
    temp_name = "appconf/appconf-header.html"
    all_product = []
    with io.open("/var/opt/adminset/main/cmdb/proj2user.json") as f:
        product = json.load(f)
        product_details = product['data']
        for detail in product_details:
            all_product.append([detail['deployNameEN'], detail['businessNameCN'], detail['deployOwnerName'],
                                detail['deployOwnerEmail'], detail['deployOwnerMobile']])
    results = {
        'temp_name': temp_name,
        'all_product': all_product,
    }
    return render(request, 'appconf/product_list.html', results)


@login_required()
@permission_verify()
def product_sync(request):
    try:
        for line in io.open('/var/opt/adminset/main/appconf/product_detail.txt', 'r+'):
            app_name, ip, port, env, deploy_method = line.split(' ')
            try:
                port = int(port)
            except ValueError:
                port = 8080
            app_and_host = Product_Detail(app_name=app_name.strip(), ip_address=ip.strip(),
                                         app_port=port, env=env.strip(), deploy_method=deploy_method.strip())
            app_and_host.save()
    except Exception as exception:
        messages.error(request, exception)
    else:
        messages.warning(request, 'app info sync successfully !!')
    return redirect('product_list')


@login_required()
@permission_verify()
def product_detail(request, app_name):
    # product_detail = Product_Detail.objects.filter(app_name=app_name)
    product_detail = Product_Detail.objects.filter(Q(app_name__startswith=app_name))

    temp_name = "appconf/appconf-header.html"
    results = {
        'app_name': app_name,
        'temp_name': temp_name,
        'product_detail': product_detail,
    }

    return render(request, 'appconf/product_detail.html', results)


@login_required
@permission_verify()
def product_detail_del(request):
    try:
        product_id = request.GET.get('id', '')
        if product_id:
            Product_Detail.objects.filter(id=product_id).delete()

        product_id_all = str(request.POST.get('product_id_all', ''))
        if product_id_all:
            for product_id in product_id_all.split(','):
                Product_Detail.objects.filter(id=product_id).delete()

    except Exception as exception:
        messages.error(request, exception)
    else:
        messages.warning(request, 'app detail delete successfully !!')
    return redirect('product_list')


@login_required
@permission_verify()
def product_detail_add(request):
    temp_name = "appconf/appconf-header.html"
    # product_detail = ''
    if request.method == 'POST':
        form = Product_Detail_Form(request.POST)
        if form.is_valid():
            app_name = form.cleaned_data['app_name']
            form.save()
            return HttpResponseRedirect(reverse('product_detail', args=[app_name]))
    else:
        app_name = request.GET.get('app_name')
        product_detail = 'show product_detail'
        form = Product_Detail_Form(initial={'app_name': app_name})

    results = {
        'form': form,
        'product_detail': product_detail,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'appconf/product_base.html', results)


@login_required
@permission_verify()
def product_del(request):
    product_id = request.GET.get('id', '')
    if product_id:
        Product.objects.filter(id=product_id).delete()

    product_id_all = str(request.POST.get('product_id_all', ''))
    if product_id_all:
        for product_id in product_id_all.split(','):
            Product.objects.filter(id=product_id).delete()

    return HttpResponseRedirect(reverse('product_list'))


@login_required
@permission_verify()
def product_add(request):
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product_list'))
    else:
        form = ProductForm()

    results = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'appconf/product_base.html', results)


@login_required
@permission_verify()
def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product_list'))
    else:
        form = ProductForm(instance=product)

    results = {
        'form': form,
        'product_id': product_id,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'appconf/product_base.html', results)


@login_required
@permission_verify()
def project_list(request, product_id):
    temp_name = "appconf/appconf-header.html"
    product = Product.objects.get(id=product_id)
    projects = product.project_set.all()
    results = {
        'temp_name': temp_name,
        'project_list':  projects,
    }
    return render(request, 'appconf/product_project_list.html', results)



