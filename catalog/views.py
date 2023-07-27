from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def homepage(request):
    return render(request, 'catalog/homepage1.html')


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts1.html')