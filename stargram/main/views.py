from django.shortcuts import render

def intro_view(request):
  return render(request, 'intro.html')