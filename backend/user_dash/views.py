from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    print('tits')
    return render(request, 'learn/dash.html')