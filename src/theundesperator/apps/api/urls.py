from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('', views.overview, name='api.api-overview'),
]

apartments_urls = [
    # ------- Rooms ------- #
    path('apartments/room/list', views.room_list, name='api.apartments-room-list'),
    path('apartments/room/detail/<int:pk>', views.room_detail, name='api.apartments-room-detail'),
    path('apartments/room/create', views.room_create, name='api.apartments-room-create'),
    path('apartments/room/update/<int:pk>', views.room_update, name='api.apartments-room-update'),
    path('apartments/room/delete/<int:pk>', views.room_delete, name='api.apartments-room-delete'),
    # ------- Apartment ------- #
    path('apartments/apartment/list', views.apartment_list, name='api.apartments-apartment-list'),
    path('apartments/apartment/detail/<int:pk>', views.apartment_detail, name='api.apartments-apartment-detail'),
    path('apartments/apartment/create', views.apartment_create, name='api.apartments-apartment-create'),
    path('apartments/apartment/update/<int:pk>', views.apartment_update, name='api.apartments-apartment-update'),
    path('apartments/apartment/delete/<int:pk>', views.apartment_delete, name='api.apartments-apartment-delete'),
    # ------- Expense ------- #
    path('apartments/expense/list', views.expense_list, name='api.apartments-expense-list'),
    path('apartments/expense/detail/<int:pk>', views.expense_detail, name='api.apartments-expense-detail'),
    path('apartments/expense/create', views.expense_create, name='api.apartments-expense-create'),
    path('apartments/expense/update/<int:pk>', views.expense_update, name='api.apartments-expense-update'),
    path('apartments/expense/delete/<int:pk>', views.expense_delete, name='api.apartments-expense-delete'),
    # ------- Item ------- #
    path('apartments/item/list', views.item_list, name='api.apartments-item-list'),
    path('apartments/item/detail/<int:pk>', views.item_detail, name='api.apartments-item-detail'),
    path('apartments/item/create', views.item_create, name='api.apartments-item-create'),
    path('apartments/item/update/<int:pk>', views.item_update, name='api.apartments-item-update'),
    path('apartments/item/delete/<int:pk>', views.item_delete, name='api.apartments-item-delete'),
]

ceremony_urls = [
    # ------- Category ------- #
    path('ceremony/category/', views.category_list, name='api.ceremony-category-list'),
    path('ceremony/category/detail/<int:pk>', views.category_detail, name='api.ceremony-category-detail'),
    path('ceremony/category/create', views.category_create, name='api.ceremony-category-create'),
    path('ceremony/category/update/<int:pk>', views.category_update, name='api.ceremony-category-update'),
    path('ceremony/category/delete/<int:pk>', views.category_delete, name='api.ceremony-category-delete'),
    # ------- Ceremony ------- #
    path('ceremony/ceremony/', views.ceremony_list, name='api.ceremony-ceremony-list'),
    path('ceremony/ceremony/detail/<int:pk>', views.ceremony_detail, name='api.ceremony-ceremony-detail'),
    path('ceremony/ceremony/create', views.ceremony_create, name='api.ceremony-ceremony-create'),
    path('ceremony/ceremony/update/<int:pk>', views.ceremony_update, name='api.ceremony-ceremony-update'),
    path('ceremony/ceremony/delete/<int:pk>', views.ceremony_delete, name='api.ceremony-ceremony-delete'),
    # ------- Music ------- #
    path('ceremony/music/', views.music_list, name='api.ceremony-music-list'),
    path('ceremony/music/detail/<int:pk>', views.music_detail, name='api.ceremony-music-detail'),
    path('ceremony/music/create', views.music_create, name='api.ceremony-music-create'),
    path('ceremony/music/update/<int:pk>', views.music_update, name='api.ceremony-music-update'),
    path('ceremony/music/delete/<int:pk>', views.music_delete, name='api.ceremony-music-delete'),
    # ------- ClothesPlanner ------- #
    path('ceremony/clothes_planner/', views.clothes_planner_list, name='api.ceremony-clothes_planner-list'),
    path('ceremony/clothes_planner/detail/<int:pk>', views.clothes_planner_detail,
         name='api.ceremony-clothes_planner-detail'),
    path('ceremony/clothes_planner/create', views.clothes_planner_create, name='api.ceremony-clothes_planner-create'),
    path('ceremony/clothes_planner/update/<int:pk>', views.clothes_planner_update,
         name='api.ceremony-clothes_planner-update'),
    path('ceremony/clothes_planner/delete/<int:pk>', views.clothes_planner_delete,
         name='api.ceremony-clothes_planner-delete'),
    # ------- Groomsman ------- #
    path('ceremony/groomsman/', views.groomsman_list, name='api.ceremony-groomsman-list'),
    path('ceremony/groomsman/detail/<int:pk>', views.groomsman_detail, name='api.ceremony-groomsman-detail'),
    path('ceremony/groomsman/create', views.groomsman_create, name='api.ceremony-groomsman-create'),
    path('ceremony/groomsman/update/<int:pk>', views.groomsman_update, name='api.ceremony-groomsman-update'),
    path('ceremony/groomsman/delete/<int:pk>', views.groomsman_delete, name='api.ceremony-groomsman-delete'),
    # ------- Guest ------- #
    path('ceremony/guest/', views.guest_list, name='api.ceremony-guest-list'),
    path('ceremony/guest/detail/<int:pk>', views.guest_detail, name='api.ceremony-guest-detail'),
    path('ceremony/guest/create', views.guest_create, name='api.ceremony-guest-create'),
    path('ceremony/guest/update/<int:pk>', views.guest_update, name='api.ceremony-guest-update'),
    path('ceremony/guest/delete/<int:pk>', views.guest_delete, name='api.ceremony-guest-delete'),
    # ------- Occasion ------- #
    path('ceremony/occasion/', views.occasion_list, name='api.ceremony-occasion-list'),
    path('ceremony/occasion/detail/<int:pk>', views.occasion_detail, name='api.ceremony-occasion-detail'),
    path('ceremony/occasion/create', views.occasion_create, name='api.ceremony-occasion-create'),
    path('ceremony/occasion/update/<int:pk>', views.occasion_update, name='api.ceremony-occasion-update'),
    path('ceremony/occasion/delete/<int:pk>', views.occasion_delete, name='api.ceremony-occasion-delete'),
    # ------- Provider ------- #
    path('ceremony/provider/', views.provider_list, name='api.ceremony-provider-list'),
    path('ceremony/provider/detail/<int:pk>', views.provider_detail, name='api.ceremony-provider-detail'),
    path('ceremony/provider/create', views.provider_create, name='api.ceremony-provider-create'),
    path('ceremony/provider/update/<int:pk>', views.provider_update, name='api.ceremony-provider-update'),
    path('ceremony/provider/delete/<int:pk>', views.provider_delete, name='api.ceremony-provider-delete'),
]

honeymoon_urls = [
    # ------- Budget ------- #
    path('honeymoon/budget/', views.budget_list, name='api.honeymoon-budget-list'),
    path('honeymoon/budget/detail/<int:pk>', views.budget_detail, name='api.honeymoon-budget-detail'),
    path('honeymoon/budget/create', views.budget_create, name='api.honeymoon-budget-create'),
    path('honeymoon/budget/update/<int:pk>', views.budget_update, name='api.honeymoon-budget-update'),
    path('honeymoon/budget/delete/<int:pk>', views.budget_delete, name='api.honeymoon-budget-delete'),
    # ------- HoneymoonOrganizer ------- #
    path('honeymoon/honeymoon_organizer/', views.honeymoon_organizer_list, name='api.honeymoon-honeymoon_organizer-list'),
    path('honeymoon/honeymoon_organizer/detail/<int:pk>', views.honeymoon_organizer_detail,
         name='api.honeymoon-honeymoon_organizer-detail'),
    path('honeymoon/honeymoon_organizer/create', views.honeymoon_organizer_create,
         name='api.honeymoon-honeymoon_organizer-create'),
    path('honeymoon/honeymoon_organizer/update/<int:pk>', views.honeymoon_organizer_update,
         name='api.honeymoon-honeymoon_organizer-update'),
    path('honeymoon/honeymoon_organizer/delete/<int:pk>', views.honeymoon_organizer_delete,
         name='api.honeymoon-honeymoon_organizer-delete'),
]

pantea_urls = [
    # ------- Decoration ------- #
    path('pantea/decoration/', views.decoration_list, name='api.pantea-decoration-list'),
    path('pantea/decoration/detail/<int:pk>', views.decoration_detail, name='api.pantea-decoration-detail'),
    path('pantea/decoration/create', views.decoration_create, name='api.pantea-decoration-create'),
    path('pantea/decoration/update/<int:pk>', views.decoration_update, name='api.pantea-decoration-update'),
    path('pantea/decoration/delete/<int:pk>', views.decoration_delete, name='api.pantea-decoration-delete'),
    # ------- PanTeaGuest ------- #
    path('pantea/pan_tea_guest/', views.pan_tea_guest_list, name='api.pantea-pan_tea_guest-list'),
    path('pantea/pan_tea_guest/detail/<int:pk>', views.pan_tea_guest_detail, name='api.pantea-pan_tea_guest-detail'),
    path('pantea/pan_tea_guest/create', views.pan_tea_guest_create, name='api.pantea-pan_tea_guest-create'),
    path('pantea/pan_tea_guest/update/<int:pk>', views.pan_tea_guest_update, name='api.pantea-pan_tea_guest-update'),
    path('pantea/pan_tea_guest/delete/<int:pk>', views.pan_tea_guest_delete, name='api.pantea-pan_tea_guest-delete'),
    # ------- PanTeaOrganizer ------- #
    path('pantea/pan_tea_organizer/', views.pan_tea_organizer_list, name='api.pantea-pan_tea_organizer-list'),
    path('pantea/pan_tea_organizer/detail/<int:pk>', views.pan_tea_organizer_detail,
         name='api.pantea-pan_tea_organizer-detail'),
    path('pantea/pan_tea_organizer/create', views.pan_tea_organizer_create, name='api.pantea-pan_tea_organizer-create'),
    path('pantea/pan_tea_organizer/update/<int:pk>', views.pan_tea_organizer_update,
         name='api.pantea-pan_tea_organizer-update'),
    path('pantea/pan_tea_organizer/delete/<int:pk>', views.pan_tea_organizer_delete,
         name='api.pantea-pan_tea_organizer-delete'),
]

urlpatterns += apartments_urls
urlpatterns += ceremony_urls
urlpatterns += honeymoon_urls
urlpatterns += pantea_urls
