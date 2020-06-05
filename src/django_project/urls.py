from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.utils.translation import ugettext as _
from django.shortcuts import render

admin.site.site_header = _('Gig2You - Administration')


def home(request):
    if request.user.is_staff:
        return redirect('admin:index')
    elif request.user.is_authenticated:
        return redirect('core:homepage')
    return render(request, 'core/other/index.html')


def contact(request):
    return render(request, 'core/other/contact.html')


def about(request):
    return render(request, 'core/other/about.html')

urlpatterns = [

    url(r'^impersonate/', include('impersonate.urls')),

    path('admin/', admin.site.urls, name='admin'),  # admin site

    path('', home, name='homepage'),
    path('about/', about, name='about'),

    path('app/', include('django_project.apps.core.urls', namespace='core')),
    path('contact/', contact, name='contact'),
    # auth
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='auth/login.html', redirect_authenticated_user=True),
         name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'),

    # password reset
    path(
        'accounts/login/password_reset/',
        auth_views.PasswordResetView.as_view(template_name='auth/reset_form.html'),
        name='password_reset',
    ),
    path(
        'accounts/login/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name="auth/reset_done.html"),
        name='password_reset_done',
    ),
    path(
        'accounts/login/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="auth/reset_confirm.html"),
        name='password_reset_confirm',
    ),
    path(
        'accounts/login/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name="auth/reset_complete.html"),
        name='password_reset_complete',
    ),
]
