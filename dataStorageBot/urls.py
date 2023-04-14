from dataStorageBot import views
from django.urls import path

urlpatterns = [
    path('', views.hello, name='hello'),
    path('tg/', views.webhook, name='tg_webhook'),
]
