from datetime import date

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from main.models import Client
from website import settings


def index(request):
    age = None
    if request.user.is_authenticated:
        today = date.today()
        birth_data = request.user.client.birthdate
        age = today.year - birth_data.year - ((today.month, today.day) < (birth_data.month, birth_data.day))
    if request.method == 'POST':
        search_str = request.POST.get('txtquery', '')
        try:
            client = Client.objects.get(name__iexact=search_str)
            age = today.year - client.birthdate.year - ((today.month, today.day) < (client.birthdate.month, client.birthdate.day))
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
            count = len(user_diseases) + len(father_diseases) + len(mother_diseases)
            if count < 6:
                mother_diseases += [None] * (6 - count)


            return render(request, 'profile_page_docteur.html', {
                'client': client,
                'user_diseases': user_diseases,
                'father_diseases': father_diseases,
                'mother_diseases': mother_diseases,
                'age': age,
            })
        except Client.DoesNotExist:
            return render(request, 'profile_page_docteur.html', {'error': 'No user found with this name.'})
    elif request.user.is_authenticated and not request.user.is_staff:
        try:
            user_diseases = request.user.client.diseases.all()
            father_diseases = []
            mother_diseases = []
            count = len(user_diseases) + len(father_diseases) + len(mother_diseases)
            if count < 6:
                mother_diseases += [None] * (6 - count)

            return render(request, 'profile_page_admin.html', {
                'client': request.user.client,
                'user_diseases': user_diseases,
                'father_diseases': father_diseases,
                'mother_diseases': mother_diseases,
                'age': age,
            })
        except Client.DoesNotExist:
            pass
    return render(request, 'profile_page_docteur.html', {'age': age, 'mother_diseases': [None] * 6})


def familypage(request):
    template = loader.get_template('family_page_admin.html')
    return HttpResponse(template.render({}, request))
