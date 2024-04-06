# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from main.forms import CombinedForm

class SignUpView(View):
    form_class = CombinedForm
    #success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request,self.template_name,{'form':form})


