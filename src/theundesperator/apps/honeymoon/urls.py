from django.shortcuts import render
from django.urls import path

from theundesperator.apps.honeymoon import views

app_name = 'honeymoon'

urlpatterns = [
    # ------- Budget ------- #
    path('honeymoon/budget/', views.budget_list, name='budget-list'),
    # path('honeymoon/budget/detail/<int:budget_id>', views.budget_detail, name='budget-detail'),
    path('honeymoon/budget/create', views.budget_create, name='budget-create'),
    path('honeymoon/budget/update/<int:budget_id>', views.budget_update, name='budget-update'),
    path('honeymoon/budget/delete/<int:budget_id>', views.budget_delete, name='budget-delete'),
    # ------- HoneymoonOrganizer ------- #
    path('honeymoon/honeymoon_organizer/', views.honeymoon_organizer_index, name='honeymoon_organizer-index'),
    # path('honeymoon/honeymoon_organizer/detail/<int:pk>', views.honeymoon_organizer_detail,
    #      name='honeymoon_organizer-detail'),
    # path('honeymoon/honeymoon_organizer/create', views.honeymoon_organizer_create,
    #      name='honeymoon_organizer-create'),
    # path('honeymoon/honeymoon_organizer/update/<int:pk>', views.honeymoon_organizer_update,
    #      name='honeymoon_organizer-update'),
    # path('honeymoon/honeymoon_organizer/delete/<int:pk>', views.honeymoon_organizer_delete,
    #      name='honeymoon_organizer-delete'),
]