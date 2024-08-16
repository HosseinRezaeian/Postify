from django.shortcuts import render,redirect
from django.views import View
from .forms import LoginForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login,logout
# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'index.html')


class Signup(View):
    def get(self, request):

        return render(request, 'sign in.html', {'form': LoginForm})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            password = form.cleaned_data['password']
            if User.objects.filter(username=username):
                return render(request, 'sign in.html', {'form': form})
            else:
                User.objects.create_user(username=username, is_staff=True,
                                         password=password)
        return redirect('home')


class Login(View):
    def get(self, request):

        return render(request, 'login.html', {'form': LoginForm})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:

                return redirect('login')

        else:

            return render(request, 'login.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('posts')
