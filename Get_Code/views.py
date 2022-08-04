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


def commit_view(request, user, name, *args, **kwargs):
    repo_name = name
    username = user

    if request.method == 'POST':
        ref_num= request.POST.getlist('ref_num')
        base = ref_num[1]
        head = ref_num[0]
        url = 'https://api.github.com/repos/%s/%s/compare/%s...%s' %(username,repo_name,base,head)
        response = requests.get(url)
        code_files = response.json()
        print(base)
        print(head)
        return render(request, 'file_name.html', context={'code_files':code_files,'repo_name':repo_name,'username':username,'head':head,'base':base})
    else:
        url = 'https://api.github.com/repos/%s/%s/commits' %(username,repo_name)
        response = requests.get(url)
        commits = response.json()
        return render(request, 'commits.html', context={'commits':commits,'repo_name':repo_name,'username':username})


def code_view(request, user, name, ref1, ref2, file, *args, **kwargs):
    username = user
    repo_name = name
    refference_head = ref1
    refference_base = ref2
    filename = file.replace("+","/")
    url1 = "https://github.com/%s/%s/raw/%s/%s" %(username,repo_name,refference_head,filename)
    r1 = requests.get(url1)
    htmlContent1 = r1.content
    soup1 = BeautifulSoup(htmlContent1, 'html.parser')
    soup_pretty1 = soup1.prettify()
    url2 = "https://github.com/%s/%s/raw/%s/%s" %(username,repo_name,refference_base,filename)
    r2 = requests.get(url2)
    htmlContent2 = r2.content
    soup2 = BeautifulSoup(htmlContent2, 'html.parser')
    soup_pretty2 = soup2.prettify()
    print(soup_pretty2)
    return render(request, 'code.html', context={'soup_pretty1':soup_pretty1,'soup_pretty2':soup_pretty2})