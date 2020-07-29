from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext as _


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('theundesperator.apps.api.urls')),
    path('', include('theundesperator.apps.core.urls')),
    path('ceremony/', include('theundesperator.apps.ceremony.urls', namespace='ceremony')),
]

admin.site.site_header = _('The UnDesperator') + ' - Admin'
admin.site.site_title = _('The UnDesperator')
admin.site.index_title = _('The UnDesperator')
