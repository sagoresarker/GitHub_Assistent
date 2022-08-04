from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Create your views here.

def index(request):
    repos=False
    if request.method == 'POST':
        username = request.POST.get('username')
        url = 'https://api.github.com/users/%s/repos' % username
        response = requests.get(url)
        repos = response.json()
    return render(request, 'index.html', context={'repos':repos})


