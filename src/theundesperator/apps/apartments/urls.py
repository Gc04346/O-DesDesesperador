from django.shortcuts import render
from django.urls import path

from theundesperator.apps.apartments import views

app_name = 'apartment'

urlpatterns = [
    # ------- Rooms ------- #
    path('room/list', views.room_list, name='room-list'),
    path('room/detail/<int:room_id>', views.room_detail, name='room-detail'),
    path('room/create', views.room_create, name='room-create'),
    # path('room/update/<int:room_id>', views.room_update, name='room-update'),
    path('room/delete/<int:room_id>', views.room_delete, name='room-delete'),
    # ------- Apartment ------- #
    path('options/list', views.apartment_list, name='apartment-list'),
    path('options/fav/<int:apartment_id>', views.set_apartment_as_favorite, name='apartment-set-favorite'),
    path('options/create', views.apartment_create, name='apartment-create'),
    path('options/details/<int:apartment_id>', views.apartment_details, name='apartment-details'),
    path('options/update/<int:apartment_id>', views.apartment_update, name='apartment-update'),
    path('options/delete/<int:apartment_id>', views.apartment_delete, name='apartment-delete'),
    # ------- Expense ------- #
    # path('expense/list', views.expense_list, name='expense-list'),
    # path('expense/detail/<int:apartment_id>', views.expense_detail, name='expense-detail'),
    path('expense/create', views.expense_create, name='expense-create'),
    # path('expense/update/<int:apartment_id>', views.expense_update, name='expense-update'),
    path('expense/delete/<int:expense_id>', views.expense_delete, name='expense-delete'),
    # ------- Item ------- #
    path('item/list', views.item_list, name='item-list'),
    # path('item/detail/<int:apartment_id>', views.item_detail, name='item-detail'),
    path('item/create', views.item_create, name='item-create'),
    # path('item/update/<int:apartment_id>', views.item_update, name='item-update'),
    path('item/delete/<int:item_id>', views.item_delete, name='item-delete'),
    path('item/mark_as_done/<int:item_id>', views.mark_unmark_item, name='item-done'),
]
