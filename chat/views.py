from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def room(request, room_name):
    return render(request, 'room_v2.html', {
        'room_name': room_name
    })