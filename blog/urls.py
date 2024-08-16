from django.urls import path

from .views import Home, Signup,Login,logout_view

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('Signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
]
