from django.contrib.auth import authenticate,login,get_user_model
from django.http import HttpResponse
from django.shortcuts import render,redirect

from .forms import ContactForm 
def home_page(request):
    #print(request.session.get("first_name","Unknown"))   #getter
    context ={
            "title" : "Welcome to shop !!",
            #"premium_content":"YEAHH"
            }
    if request.user.is_authenticated:
        context["premium_content"]="YEAHH"
    return render(request,"home_page.html",context)
def about_page(request):
    context ={
            "title":"About Page"
            }
    return render(request,"home_page.html",context)
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context ={
            "title":"Contact Page",
            "form": contact_form,
            #"brand": "new Brand Name"
            }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    if request.method == "POST":                                           # NOT shown in terminal
        print(request.POST)
        print(request.POST.get('fullname'))
    return render(request,"contact/view.html",context)
