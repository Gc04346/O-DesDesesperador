from django.urls import path
from django_project.apps.core import views

app_name = 'core'


urlpatterns = [
    path('home/', views.homepage, name='homepage'),
    path('profile/', views.profile, name='myprofile'),
    path('accept_terms/', views.accept_terms, name='acceptterms'),
    path('preregister/', views.producers_pre_register, name='preregister'),
    path('activate/<int:user_id>', views.activate_user, name='activate_user'),
    path('faq/', views.faq, name='faq'),
    path('message/<int:event_id>', views.send_message, name='sendmessage'),
    path('message/<int:comment_id>/delete/<int:event_id>', views.delete_message, name='deletemessage'),

    # musician-event confirmation / refusal
    path('musicianevent/confirmation/<int:musician_event_id>', views.add_musicians_confirmation, name='musicianconfirmation'),
    path('musicianevent/refusal/<int:musician_event_id>', views.add_musicians_refusal, name='musicianrefusal'),

    # musician related urls
    path('musician/management/', views.create_or_edit_musician, name='musicianmanagement'),
    path('musician/list/', views.musicians_list, name='musicianslist'),
    path('musician/delete/<int:musician_id>/', views.delete_musician, name='musiciandelete'),
    path('musician/addto/<int:event_id>/', views.add_musicians, name='addmusicians'),
    path('references/manage/<int:event_id>/', views.set_references_for_musicians, name='managereferencesforevent'),

    # event related urls
    path('event/history/', views.pastevents, name='pastevents'),
    path('event/<int:event_id>/', views.event, name='event'),
    path('event/new/', views.new_event, name='newevent'),
    path('event/confirm/<int:event_id>/', views.event_confirmed, name='eventconfirmed'),
    path('event/cancel/<int:event_id>/', views.event_cancelled, name='eventcancelled'),
    path('event/conclude/<int:event_id>/', views.conclude_event, name='eventconcluded'),
    path('event/paid/<int:event_id>/', views.event_paid, name='paymentconfirmed'),
    path('event/refused/<int:event_id>/', views.event_refused, name='refuseparticipation'),

    # artist song-management related urls
    path('song/list/', views.my_songs, name='my_songs'),
    path('song/manage/', views.manage_songs, name='songmanagement'),
    path('song/delete/<int:song_id>/', views.song_delete, name='songdelete'),
]
