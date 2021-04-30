from django.shortcuts import render

# La page d'accueil                                                                                 
def index(request):
    return render(request, 'zhome/index.html', None)
