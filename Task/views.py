from django.shortcuts import render

# Create your views here.

def homepage(request):
    context_dict = {}
    context_dict['username'] = 'User'
    return render(request, 'homepage.html', context=context_dict)