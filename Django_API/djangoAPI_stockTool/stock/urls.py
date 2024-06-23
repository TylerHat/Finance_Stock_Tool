from django.urls import path
from . import views

urlpatterns = [
    path('bollinger-rsi/', views.bollinger_rsi_view, name='bollinger_rsi'),
]
