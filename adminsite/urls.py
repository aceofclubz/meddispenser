from django.urls import path
from . import views
urlpatterns = [
        path('', views.index, name='index'),
        path('login', views.login, name='login'),
        path('logout', views.logout, name='logout'),
        path('users', views.users, name='user'),
        path('medicine', views.medicine, name='medicine'),
        path('transactions', views.transact, name='transactions_all'),
        path('transactions/users/<str:user_id>', views.transact_u, name='transactions_users'),
        path('transactions/medicine/<int:med_id>', views.transact_med, name='transactions_med'),
        path('create', views.user_c, name='create'),
        path('create/<int:for_admin>', views.user_c, name='create'),
        path('edit/<str:user_id>', views.user_u, name='update'),
        path('edit/<str:user_id>/<int:for_admin>', views.user_u, name='update'),
        ]
