from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from main.models import Client
from website import settings


def index(request):
    if request.method == 'POST':
        search_str = request.POST.get('txtquery', '')
        try:
            client = Client.objects.get(name__iexact=search_str)
            user_diseases = client.diseases.all()
            father_diseases = []
            mother_diseases = []
            if client.father_name:
                try:
                    father = Client.objects.get(name__iexact=client.father_name)
                    father_diseases = father.diseases.all()
                except Client.DoesNotExist:
                    pass
            if client.mother_name:
                try:
                    mother = Client.objects.get(name__iexact=client.mother_name)
                    mother_diseases = mother.diseases.all()
                except Client.DoesNotExist:
                    pass

            return render(request, 'profile_page_admin.html', {
                'client': client,
                'user_diseases': user_diseases,
                'father_diseases': father_diseases,
                'mother_diseases': mother_diseases,
            })
        except Client.DoesNotExist:
            return render(request, 'profile_page_admin.html', {'error': 'No user found with this name.'})
    else:
        return render(request, 'profile_page_admin.html')


def familypage(request):
    template = loader.get_template('family_page_admin.html')
    return HttpResponse(template.render({}, request))
