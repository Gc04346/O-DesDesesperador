from django.shortcuts import render
from django.urls import path

from theundesperator.apps.ceremony import views

app_name = 'ceremony'

urlpatterns = [
    # ------- Category ------- #
    # path('category/', views.category_list, name='ceremony-category-list'),
    # path('category/detail/<int:pk>', views.category_detail, name='ceremony-category-detail'),
    path('category/create', views.category_create, name='ceremony-category-create'),
    # path('category/update/<int:pk>', views.category_update, name='ceremony-category-update'),
    path('category/delete/<int:category_id>', views.category_delete, name='ceremony-category-delete'),
    # ------- Ceremony ------- #
    path('', views.ceremony_index, name='ceremony-index'),
    # path('ceremony/detail/<int:pk>', views.ceremony_detail, name='ceremony-ceremony-detail'),
    # path('ceremony/create', views.ceremony_create, name='ceremony-ceremony-create'),
    # path('ceremony/update/<int:pk>', views.ceremony_update, name='ceremony-ceremony-update'),
    # path('ceremony/delete/<int:pk>', views.ceremony_delete, name='ceremony-ceremony-delete'),
    # ------- Music ------- #
    path('music/', views.music_list, name='ceremony-music-list'),
    # path('music/detail/<int:pk>', views.music_detail, name='ceremony-music-detail'),
    path('music/create', views.music_create, name='ceremony-music-create'),
    path('music/update/<int:music_id>', views.music_update, name='ceremony-music-update'),
    path('music/delete/<int:music_id>', views.music_delete, name='ceremony-music-delete'),
    # ------- ClothesPlanner ------- #
    path('clothes_planner/', views.clothes_planner, name='ceremony-clothes_planner-list'),
    # path('clothes_planner/detail/<int:pk>', views.clothes_planner_detail,
    #      name='ceremony-clothes_planner-detail'),
    # path('clothes_planner/create', views.clothes_planner_create, name='ceremony-clothes_planner-create'),
    # path('clothes_planner/update/<int:pk>', views.clothes_planner_update,
    #      name='ceremony-clothes_planner-update'),
    # path('clothes_planner/delete/<int:pk>', views.clothes_planner_delete,
    #      name='ceremony-clothes_planner-delete'),
    # ------- Groomsman ------- #
    path('groomsman/', views.groomsman_list, name='ceremony-groomsman-list'),
    # path('groomsman/detail/<int:pk>', views.groomsman_detail, name='ceremony-groomsman-detail'),
    path('groomsman/create', views.groomsman_create, name='ceremony-groomsman-create'),
    path('groomsman/update/<int:groomsman_id>', views.groomsman_update, name='ceremony-groomsman-update'),
    path('groomsman/delete/<int:groomsman_id>', views.groomsman_delete, name='ceremony-groomsman-delete'),
    # ------- Guest ------- #
    path('guest/', views.guests_list, name='ceremony-guest-list'),
    path('guest/add', views.guest_create, name='ceremony-guest-create'),
    path('guest/update/<int:guest_id>', views.guest_update, name='ceremony-guest-update'),
    path('guest/delete/<int:guest_id>', views.guest_delete, name='ceremony-guest-delete'),
    # ------- Occasion ------- #
    # path('occasion/', views.occasion_list, name='ceremony-occasion-list'),
    # path('occasion/detail/<int:pk>', views.occasion_detail, name='ceremony-occasion-detail'),
    path('occasion/create', views.occasion_create, name='ceremony-occasion-create'),
    # path('occasion/update/<int:pk>', views.occasion_update, name='ceremony-occasion-update'),
    path('occasion/delete/<int:pk>', views.occasion_delete, name='ceremony-occasion-delete'),
    # ------- Provider ------- #
    path('provider/', views.provider_list, name='ceremony-provider-list'),
    path('provider/fav/<int:provider_id>', views.set_provider_as_favorite, name='ceremony-provider-set-favorite'),
    # path('provider/detail/<int:pk>', views.provider_detail, name='ceremony-provider-detail'),
    path('provider/create', views.provider_create, name='ceremony-provider-create'),
    path('provider/update/<int:provider_id>', views.provider_update, name='ceremony-provider-update'),
    path('provider/delete/<int:provider_id>', views.provider_delete, name='ceremony-provider-delete'),
]
