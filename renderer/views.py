from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse

# Create your views here.


def index(request):
    if request.user.is_authenticated:
      return render(request, "main/index.html")
    else:
      return HttpResponseRedirect(reverse('login'))


def redirect(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))

def login(request):
    return HttpResponse("Redirected to Login page")

def assignment(request):
  return HttpResponse("Hello, world. 5f123c60 is the polls index.")