from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

def index(request):
    template = loader.get_template('profile_page_admin.html')
    return HttpResponse(template.render({},request))

# Create your views here.

