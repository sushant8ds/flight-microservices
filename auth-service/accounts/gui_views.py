from django.shortcuts import render
from .models import User

def account_list(request):
    accounts = User.objects.all()
    return render(request, 'accounts/gui_account_list.html', {'accounts': accounts})
