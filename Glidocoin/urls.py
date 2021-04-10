from django.urls import path
from . import views

urlpatterns = [
    path('startMiner/<wallet_addr>/', views.startMainer),
    path('stopMiner/<wallet_addr>/', views.stopMainer),
    path('balance/<wallet_addr>/', views.getBalanceOf),
    path('Glidocoin-start/', views.init),
    path('myWallet/', views.getWallet),
    path('', views.home),
]