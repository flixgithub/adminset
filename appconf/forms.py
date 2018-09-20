#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *
from .models import Product, Project, AppOwner, AuthInfo, Product_Detail


class AuthInfoForm(forms.ModelForm):

    class Meta:
        model = AuthInfo
        exclude = ("id",)
        widgets = {
            'dis_name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'username': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'password': TextInput(attrs={'class': 'form-control', 'type': 'password', 'style': 'width:450px'}),
            'private_key': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'memo': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class AppOwnerForm(forms.ModelForm):

    class Meta:
        model = AppOwner
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'phone': TextInput(attrs={'class': 'form-control','style': 'width:450px'}),
            'qq': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'weChat': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'description': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px'}),
            'owner': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class Product_Detail_Form(forms.ModelForm):

    class Meta:
        model = Product_Detail
        exclude = ("id",)
        widgets = {
            'app_name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'ip_address': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'app_port': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'env': Select(choices=(('cloud_dev','cloud_dev'),('cloud_qa','cloud_qa'),('cloud_pp','cloud_pp'),('cloud_prd','cloud_prd'),
                                   ('psa_dev','psa_dev'),('psa_qa','psa_qa'), ('psa_pp','psa_pp'), ('psa_prd','psa_prd'),
                                   ('fd_dev','fd_dev'), ('fd_qa','fd_qa'), ('fd_pp','fd_pp'), ('fd_prd','fd_prd'),
                                   ('gz_dev','gz_dev'), ('gz_qa','gz_qa'), ('gz_pp','gz_pp'), ('gz_prd','gz_prd'),
                                   ('wl_dev','wl_dev'), ('wl_qa','wl_qa'), ('wl_pp','wl_pp'), ('wl_prd','wl_prd'),
                                   ),
                          attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'deploy_method': Select(choices=(('war','war'),('jar','jar'),('container','container'),('shell','shell'),('na','n/a')),
                                    attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'description': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px'}),
            'language_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'server_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_arch': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'appPath': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'source_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'source_address': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'configPath': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'product': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'owner': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'serverList': forms.SelectMultiple(attrs={'class': 'form-control', 'size':'10', 'multiple': 'multiple'}),
        }
