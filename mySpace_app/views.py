import imp
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Student

# Create your views here.
def show_login_page(request):
    return render(request,"login_page.html")

def do_login(request):
    user = authenticate(username=request.POST.get("username"),password=request.POST.get("password"))
    if user!=None:
        login(request, user)
        #print(dir(user))
        if user.is_superuser:
            return HttpResponseRedirect('/admin')
        elif Student.objects.filter(user=request.user).exists():
            return HttpResponseRedirect(reverse("student_home"))
        else:
            return HttpResponseRedirect(reverse("faculty_home"))
    else:
        messages.error(request,"Invalid Login Credentials")
        return HttpResponseRedirect("/")


#Faculty views

def faculty_home(request):
    return render(request, "faculty_templates/faculty_home.html")

#Student views

def student_home(request):
    return render(request, "student_templates/student_home.html")