from django.contrib.auth import authenticate,login,get_user_model
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from .forms import LoginForm ,RegisterForm,GuestForm
from .models import GuestEmail

# Create your views here.

def guest_register_view(request):
    form=GuestForm(request.POST or None)
    context = {
            "form":form
            }
    #print("User logged in")
    #print(request.user.is_authenticated)                            #    Not shown in terminal   #will return false
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(url = redirect_path ,allowed_hosts=request.get_host()):
            return redirect(redirect_path)                                       ### in url in browser have to write login?next=https://......  ---->>> complete url
        else:
            return redirect("https://greckle.io/goel_enterprises/register/")
    return redirect("https://greckle.io/goel_enterprises/register/")


def login_page(request):
    form=LoginForm(request.POST or None)
    context = {
            "form":form
            }
    #print("User logged in")
    #print(request.user.is_authenticated)                            #    Not shown in terminal   #will return false
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        #print(form.cleaned_data)
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(request,username=username,password=password)
        #print(request.user.is_authenticated)
        #print(user)
        if user is not None:
            #print(request.user.is_authenticated)             #check again if return false   #only return true after nextline in code i.e. login(..)
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            #print(request.user.is_authenticated)
            #context['form']=LoginForm()
            if is_safe_url(url = redirect_path ,allowed_hosts=request.get_host()):
                return redirect(redirect_path)                                       ### in url in browser have to write login?next=https://......  ---->>> complete url
            else:
                return redirect("https://greckle.io/goel_enterprises/login")
        else:
            print("Error")
    return render(request,"accounts/login.html",context)


User = get_user_model()
def register_page(request):
    form=RegisterForm(request.POST or None)
    context={
            "form":form
            }
    if form.is_valid():
        print(form.cleaned_data)
        username=form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password=form.cleaned_data.get("password")
        new_user=User.objects.create_user(username,email,password)
        print(new_user)
    return render(request,"accounts/register.html",context)
