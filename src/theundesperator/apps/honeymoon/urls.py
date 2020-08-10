from django.urls import path

from theundesperator.apps.honeymoon import views

app_name = 'honeymoon'

urlpatterns = [
    # ------- Budget ------- #
    path('budget/', views.budget_list, name='budget-list'),
    # path('budget/detail/<int:budget_id>', views.budget_detail, name='budget-detail'),
    path('budget/create', views.budget_create, name='budget-create'),
    path('budget/update/<int:budget_id>', views.budget_update, name='budget-update'),
    path('budget/delete/<int:budget_id>', views.budget_delete, name='budget-delete'),
    # ------- HoneymoonOrganizer ------- #
    path('index/', views.honeymoon_organizer_index, name='honeymoon_organizer-index'),
    # path('honeymoon_organizer/detail/<int:pk>', views.honeymoon_organizer_detail,
    #      name='honeymoon_organizer-detail'),
    # path('honeymoon_organizer/create', views.honeymoon_organizer_create,
    #      name='honeymoon_organizer-create'),
    # path('honeymoon_organizer/update/<int:pk>', views.honeymoon_organizer_update,
    #      name='honeymoon_organizer-update'),
    # path('honeymoon_organizer/delete/<int:pk>', views.honeymoon_organizer_delete,
    #      name='honeymoon_organizer-delete'),
]