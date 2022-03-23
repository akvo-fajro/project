from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm,ChangePasswordForm

# Create your views here.
@login_required(login_url='login')
def change_password_view(request,*args,**kargs):
    form = ChangePasswordForm()
    err = False
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            err = True
        else:
            user = User.objects.get(username=request.user)
            user.set_password(password1)
            user.save()
            logout(request)
            return redirect('/accounts/login')
    context = {
        'form':form,
        'error':err
    }
    return render(request,'users_pages/users_change_password.html',context)

def homepage_view(request,*args,**kargs):
    return render(request,'users_pages/users_home.html',{})


def login_view(request,*args,**kargs):
    form = LoginForm()
    err = False
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            if 'next' in request.GET.keys():
                return redirect(request.GET.get('next'))
            return redirect('/')
        else:
            err = True
    context = {
        'form':form,
        'error':err,
    }
    return render(request,'users_pages/users_login.html',context)


def logout_view(request,*args,**kargs):
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def profile_view(request,*args,**kargs):
    return render(request,'users_pages/users_profile.html',{})