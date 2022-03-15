from django.shortcuts import render

# Create your views here.
def ShowLoginPage(request):
    return render(request,"login_page.html")