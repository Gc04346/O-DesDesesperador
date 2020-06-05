from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models.base import Producer, Artist, MusicianEvent, Musician, MusicDirector, Event, ArtistSong, EventSong, \
    FaqModel, Comment


admin.site.register(MusicianEvent)
admin.site.register(ArtistSong)
admin.site.register(EventSong)
admin.site.register(FaqModel)
admin.site.register(Comment)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    readonly_fields = ['total_price',]
    list_filter = [
        'is_active',
        'is_finalized',
        'event_alright',
        'date',
        'event_time',
        'region',
    ]
    search_fields = [
        'artist',
        'producer',
        'music_director',
        'region',
        'date',
        'event_time',
    ]
    list_display = [
        'name',
        'region',
        'producer',
        'artist',
        'date',
        'is_finalized',
    ]
    # fields = [
        # 'is_active',
        # 'name',
        # 'producer',
        # 'event_type',
        # 'date',
        # 'event_time',
        # 'presentation_date',
        # 'presentation_time',
        # 'region',
        # 'address',
        # 'cep',
        # 'distance_from_downtown',
        # 'artist',
        # 'artist_confirmation',
        # 'music_director',
        # 'confirmed',
        # 'dm_rate',
        # 'notes',
        # 'dm_fee',
        # 'platform_fee',
        # 'total_musicians_fee',
        # 'total_musicians_transportation_fee',
        # 'total_price',
        # 'paid_ammount',
        # 'payment_date',
        # 'invoice_number',
        # 'payment_method',
        # 'dm_payment_received',
        # 'platform_payment_received',
        # 'total_musicians_payment_received',
        # 'payment_allocated',
        # 'attendants_list_ok',
        # 'event_alright',
        # 'is_finalized',
        # 'post_event_comments',
    # ]
    fieldsets = [
        (_('General Info'), {
            'classes': ('grp-collapse grp-open',),
            'fields': [
                'is_active',
                'name',
                'producer',
                'event_type',
                'date',
                'event_time',
                'presentation_date',
                'presentation_time',
                'artist',
                'artist_confirmation',
                'music_director',
                'confirmed',
                'dm_rate',
                'notes',
            ]
        }),
        (_('Location'), {
            'classes': ('grp-collapse grp-open',),
            'fields': [
                'region',
                'address',
                'cep',
                'distance_from_downtown',
            ]
        }),
        (_('Pricing'), {
            'classes': ('grp-collapse grp-open',),
            'fields': [
                'dm_fee',
                'platform_fee',
                'total_musicians_fee',
                'total_musicians_transportation_fee',
                'total_price',
                'paid_ammount',
                'payment_date',
                'invoice_number',
                'payment_method',
                'dm_payment_received',
                'platform_payment_received',
                'total_musicians_payment_received',
                'payment_allocated',
            ]
        }),
        (_('Event Conclusion'), {
            'classes': ('grp-collapse grp-open',),
            'fields': [
                'attendants_list_ok',
                'event_alright',
                'is_finalized',
                'post_event_comments',
            ]
        }),
    ]

    def total_price(self, obj):
        return 'R$ {}'.format(obj.total_price())

    total_price.short_description = _('Total Price')

@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    readonly_fields = [
        'get_user_object_data',
    ]
    fields = [
        'name',
        'email',
        'phone',
        'whatsapp',
        'music_director',
        'instrument',
        'address',
        'cep',
        'doc_number',
        'accepted_use_terms',
        'get_user_object_data',
    ]

    def get_user_object_data(self, obj):
        user = User.objects.get(id=obj.id)
        return format_html(
            '<span>{} - {}</span></br><span>{} - {}</span></br><span>{} - {}</span></br><span>{} - {}</span></br>'.format(
                _('Is Active'), user.is_active, _('Is Staff'), user.is_staff, _('Last Login'), user.last_login,
                _('Date Joined'), user.date_joined))

    get_user_object_data.short_description = _('User Details')
    get_user_object_data.allow_tags = True
    list_display = ['name', 'email', 'music_director', 'instrument']
    list_filter = ['music_director', 'user__is_active']
    search_fields = ['name', 'email']


def get_action_html(obj):
    try:
        user = User.objects.get(id=obj.user_id)
    except ObjectDoesNotExist as e:
        return e
    if user.is_active:
        return _('User is already activated.')
    else:
        return format_html('<a class="button default" style="float:none" href="{}">{}</a></br><small>{}</small>',
                           reverse('core:activate_user', kwargs={'user_id': user.id}),
                           _('Activate User'), _('Activate the user profile here.'))


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    readonly_fields = [
        'make_active',
    ]
    fields = [
        'name',
        'email',
        'phone',
        'whatsapp',
        'address',
        'cep',
        'doc_number',
        'accepted_use_terms',
        'make_active',
    ]
    search_fields = ['name', 'email']
    list_filter = ['user__is_active']

    def make_active(self, obj):
        try:
            return get_action_html(obj)
        except Exception as e:
            return e

    make_active.short_description = _('Activate User')
    make_active.allow_tags = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # do not show artists
        return qs.filter(user__artist__isnull=True)


@admin.register(MusicDirector, Artist)
class DeafulUserAdmin(admin.ModelAdmin):
    # readonly_fields = [
    #     'address',
    #     'cep',
    #     'doc_number',
    #     'accepted_use_terms',
    # ]
    exclude = ['user']
    list_filter = ['user__is_active']
    search_fields = ['name', 'email']


# @admin.register(Artist)
# class ArtistUserAdmin(DeafulUserAdmin):
#     exclude = ['user', 'reference']


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from impersonate.admin import UserAdminImpersonateMixin


class NewUserAdmin(UserAdminImpersonateMixin, UserAdmin):
    open_new_window = True
    pass


admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
