from django.urls import path, include
from . import views
urlpatterns = [
        path('', views.index, name='index'),
        path('login', views.login, name='login'),
        path('users', views.users, name='user'),
        path('transactions', views.transact, name='transactions_all'),
        path('transactions/users/<int:user_id>', views.transact_u, name='transactions_users'),
        path('transactions/medicine/<int:med_id>', views.transact_med, name='transactions_med'),
        ]
