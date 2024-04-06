from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from main.models import Client
from website import settings


def index(request):
    context = {}
    if request.method == 'POST':
        result = Client.objects.filter(user__username__iexact=request.POST.get('txtquery'))
        if result.exists():
            context['result'] = result
        else:
            context['error'] = 'No results found'
    return render(request, 'profile_page_admin.html', context)

# Create your views here.

def familypage(request):
    template = loader.get_template('family_page_admin.html')
    return HttpResponse(template.render({}, request))
