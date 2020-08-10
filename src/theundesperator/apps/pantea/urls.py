from django.urls import path

from theundesperator.apps.pantea import views

app_name = 'pantea'

urlpatterns = [
    # ------- Decoration ------- #
    path('decoration/', views.decoration_list, name='decoration-list'),
    path('decoration/create', views.decoration_create, name='decoration-create'),
    path('decoration/create', views.notemplate_decoration_create, name='notemplate-decoration-create'),
    # path('decoration/update/<int:pk>', views.decoration_update, name='decoration-update'),
    path('decoration/delete/<int:decoration_id>', views.decoration_delete, name='decoration-delete'),
    # ------- PanTeaGuest ------- #
    path('pan_tea_guest/', views.pan_tea_guest_list, name='pan_tea_guest-list'),
    # path('pan_tea_guest/detail/<int:pk>', views.pan_tea_guest_detail, name='pan_tea_guest-detail'),
    path('pan_tea_guest/create', views.pan_tea_guest_create, name='pan_tea_guest-create'),
    path('pan_tea_guest/update/<int:pan_tea_guest_id>', views.pan_tea_guest_update, name='pan_tea_guest-update'),
    path('pan_tea_guest/delete/<int:pan_tea_guest_id>', views.pan_tea_guest_delete, name='pan_tea_guest-delete'),
    # ------- PanTeaOrganizer ------- #
    path('index/', views.pan_tea_index, name='index'),
    # path('pan_tea_organizer/detail/<int:pk>', views.pan_tea_organizer_detail,
    #      name='pan_tea_organizer-detail'),
    # path('pan_tea_organizer/create', views.pan_tea_organizer_create, name='pan_tea_organizer-create'),
    # path('pan_tea_organizer/update/<int:pk>', views.pan_tea_organizer_update,
    #      name='pan_tea_organizer-update'),
    # path('pan_tea_organizer/delete/<int:pk>', views.pan_tea_organizer_delete,
    #      name='pan_tea_organizer-delete'),
]