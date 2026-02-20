from django.urls import path
from . import views

app_name = 'auths'

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-out/', views.sign_out, name='sign_out'),

    path('user/profile/', views.profile_view, name='profile'),
    path('user/edit-profile/', views.edit_profile_view, name='edit_profile'),
]
