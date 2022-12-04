from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('<int:id>', views.detail, name='detail')
]
