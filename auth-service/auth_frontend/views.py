from django.shortcuts import render
from accounts.models import User

def index(request):
    return render(request, 'index.html')

def accounts_list(request):
    accounts = User.objects.all()
    return render(request, 'accounts.html', {'accounts': accounts})
