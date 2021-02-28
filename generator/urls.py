from django.urls import path

from . import views

app_name = 'generator'
urlpatterns = [
    path('', views.index, name='index'),
    path('generate_quote_box', views.generate_quote_box, name='generate_quote_box'),
]