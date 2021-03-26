from Web.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django import template
from django.contrib import auth
from django.contrib.auth import logout
import time
import os
from django.shortcuts import redirect
from django.contrib import messages

register = template.Library()



@register.filter(name="has_group")
def has_group(usuario,grupo):
    return usuario.groups.filter(name__exact=grupo).exists()

@register.filter
def listar(n):
    return [i+1 for i in range(0,n)]





