from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
import datetime

from django.forms import BaseInlineFormSet
from django.forms.widgets import TextInput
from django.utils.translation import ugettext as _

from django_project.apps.core.models import Artist, MusicDirector, MusicianEvent, Event
from django.contrib.auth.models import User

from django_project.apps.core.models.base import INSTRUMENTS, ArtistSong, EventSong, Musician, \
    get_instrument_name_by_type


class CommentForm(forms.Form):
    """
        Formulario para comentarios dm/artista em um evento
    """
    message = forms.CharField()
    author_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    created_date = forms.DateTimeField(required=False, widget=forms.HiddenInput())
    event_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    # usado para preencher os campos automaticos do comentario
    def set_data(self, user, event):
        self.cleaned_data['event_id'] = event.id
        self.cleaned_data['created_date'] = datetime.datetime.now()
        self.cleaned_data['author_id'] = user.id


class UserBaseForm(forms.Form):
    """
        Formulario para gerenciamento do usuario padrao
    """
    email = forms.EmailField(label=_('Email'))  # usado apenas para modificar/criar o usuario

    name = forms.CharField(label=_('Name'))

    phone = forms.CharField(label=_('Phone'))
    whatsapp = forms.CharField(label=_('Whatsapp'))

    address = forms.CharField(max_length=250)
    cep = forms.CharField(max_length=10)
    doc_number = forms.CharField(max_length=14)

    password = forms.CharField(required=False, widget=forms.PasswordInput(), label=_('Password'),
                               help_text=_('Enter only to update.'))
    password_confirmation = forms.CharField(required=False, widget=forms.PasswordInput(), label=_('Confirm password'),
                                            help_text=_('Confirm to update.'))

    def clean(self):
        cleaned_data = super().clean()
        # confere se o email ja existe
        if cleaned_data.get('user_id', False):
            if User.objects.filter(username=cleaned_data['email']).exclude(id=cleaned_data['user_id']).exists():
                self.add_error(field='email',
                               error=ValidationError(
                                   _('This email is being used. Please enter another one.')))
        else:
            if User.objects.filter(username=cleaned_data['email']).exists():
                self.add_error(field='email',
                               error=ValidationError(
                                   _('This email is being used. Please enter another one.')))
        # confere se as senhas foram preenchidas e batem
        if (cleaned_data['password'] != '' or cleaned_data['password_confirmation'] != '') and cleaned_data[
            'password'] != cleaned_data['password_confirmation']:
            self.add_error(field='password_confirmation',
                           error=ValidationError(
                               _('Passwords don\'t match.')))


class UserForm(UserBaseForm):
    """
        Formulario especifico para criacao de usuarios
    """
    user_id = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, is_artist: bool = False, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # se o usuario for artista, preenche os campos de aceitacao de instrumento
        if is_artist:
            self.fields['accept_v'] = forms.BooleanField(label=_('Accept Guitar'), required=False)
            self.fields['accept_g'] = forms.BooleanField(label=_('Accept Eletric Guitar'), required=False)
            self.fields['accept_b'] = forms.BooleanField(label=_('Accept Bass'), required=False)
            self.fields['accept_t'] = forms.BooleanField(label=_('Accept Keyboard'), required=False)
            self.fields['accept_bt'] = forms.BooleanField(label=_('Accept Drums'), required=False)
            self.fields['accept_bvt'] = forms.BooleanField(label=_('Accept Backing Vocal (Tenor)'),
                                                           required=False)
            self.fields['accept_bvs'] = forms.BooleanField(label=_('Accept Backing Vocal (Soprano)'),
                                                           required=False)
            self.fields['accept_bvc'] = forms.BooleanField(label=_('Accept Backing Vocal (Contralto)'),
                                                           required=False)


class CreateMusicianForm(forms.Form):
    """
        Formulario de criacao de musico
    """
    music_director_id = forms.CharField(
        widget=forms.HiddenInput())  # usado apenas para identificar o musico a ser alterado
    musician_id = forms.CharField(widget=forms.HiddenInput(),
                                  required=False)  # usado apenas para identificar o musico a ser alterado
    email = forms.EmailField(label=_('Email'))  # usado apenas para modificar/criar o usuario
    name = forms.CharField(label=_('Name'))
    phone = forms.CharField(label=_('Phone'))
    whatsapp = forms.CharField(label=_('Whatsapp'))
    instrument = forms.ChoiceField(label=_('Instrument'), choices=INSTRUMENTS)

    # confere se o email ja esta sendo usado
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', None)
        musician_id = cleaned_data.get('musician_id', None)
        if musician_id:
            email_is_used = User.objects.filter(username=email).exclude(musician__id=musician_id).exists()
        else:
            email_is_used = User.objects.filter(username=email).exists()

        if email_is_used:
            raise ValidationError(_('This email is being used. Please enter another one.'))


class RawEventForm(forms.Form):
    """
        Formulario de criacao de evento
    """
    from django_project.apps.core.models.base import EVENT_TYPES

    name = forms.CharField(label=_('Event name'), max_length=40)
    date = forms.DateField(widget=DatePickerInput(), label=_('Event date'), required=True)
    event_time = forms.TimeField(widget=TimePickerInput(), label=_('Event start time'), required=True)
    presentation_date = forms.DateField(widget=DatePickerInput(), label=_('Sound testing date'), required=True)
    presentation_time = forms.TimeField(widget=TimePickerInput(), label=_('Sound testing time'), required=True)
    event_type = forms.ChoiceField(choices=EVENT_TYPES, label=_('Event type'))
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), label=_('Artist'))
    producer_id = forms.IntegerField(required=False)
    instruments = forms.MultipleChoiceField(label=_('Choose the necessary instruments'), choices=INSTRUMENTS,
                                            widget=forms.SelectMultiple(attrs={
                                                "class": "multiselect_custom"
                                            }))
    notes = forms.CharField(required=False,
                            label=_('Notes'),
                            widget=forms.Textarea(
                                attrs={
                                    'placeholder': _('Additional information about your new awesome event'),
                                    'rows': 3,
                                }
                            ))
    address = forms.CharField(max_length=250, label=_('Event Address'))
    cep = forms.CharField(max_length=10, label=_('CEP'))
    distance = forms.IntegerField(min_value=0, max_value=150, label=_('Distance from Downtown (in Km)'),
                                  help_text=_('You can create events up to 150km from downtown'))

    # produtor eh um campo automatico. Aqui se define ele
    def setProducer(self, user):
        self.cleaned_data['producer_id'] = user.producer.id

    # o init eh usado para preencher as opcoes de regioes para o evento
    def __init__(self, *args, **kwargs):
        super(RawEventForm, self).__init__(*args, **kwargs)
        self.fields['music_director_id'] = forms.ChoiceField(
            choices=[[music_director.id, music_director.region] for music_director in
                     MusicDirector.get_all_active_music_directors()], label=_('Region:')
        )

    # validacoes das datas e instrumentos
    def clean(self):
        cleaned_data = super(RawEventForm, self).clean()
        presentation_date = cleaned_data.get('presentation_date', None)
        date = cleaned_data.get('date', None)
        event_time = cleaned_data.get('event_time', None)
        presentation_time = cleaned_data.get('presentation_time', None)
        if presentation_date > date or (presentation_date == date and presentation_time > event_time):
            self.add_error(field=NON_FIELD_ERRORS,
                           error=ValidationError(
                               _('Presentation date and time should be earlier than event date and time.')))
        artist = cleaned_data['artist']
        for instrument in cleaned_data['instruments']:
            if not getattr(artist, 'accept_' + instrument, False):
                self.add_error(field=NON_FIELD_ERRORS, error=ValidationError(
                    '{}: {}.'.format(_('Artist does not allow'), get_instrument_name_by_type(instrument))))


class AbstractReferenceForm(forms.ModelForm):
    """
        Formulario generico de criacao de referencias
    """
    reference_id = forms.IntegerField(widget=forms.HiddenInput(),
                                      required=False)  # usado apenas para identificar o musico a ser alterado


class ArtistReferenceForm(AbstractReferenceForm):
    """
        Formulario especifico de criacao de referencias do artista pro diretor
    """
    class Meta:
        model = ArtistSong
        fields = ('artist_id', 'name', 'file', 'links', 'notes')

    artist_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    # define o campo automatico do artista
    def setArtist(self, user):
        self.cleaned_data['artist_id'] = user.artist.id


class EventReferenceForm(AbstractReferenceForm):
    """
        Formulario especifico de criacao de referencias para os musicos
    """
    class Meta:
        model = EventSong
        fields = ('event_id', 'name', 'file', 'links', 'notes')

    event_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    # define o campo automatico do evento
    def setEvent(self, event):
        self.cleaned_data['event_id'] = event.id


class MusicianEventForm(forms.ModelForm):
    """
        Formulario de criacao do MusicianEvent, para ligar o musico ao evento
    """
    instrument_for_humans = forms.CharField(disabled=True, required=False, label='', widget=TextInput(
        attrs={'class': 'data-hide_and_show_value'}))

    # instrument for humans eh usado pra pegar o nome do instrumento traduzido e com a informacao de musico princ/sub
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        if instance:
            kwargs['initial'] = {'instrument_for_humans': instance.instrument_for_humans(), }
            super().__init__(*args, **kwargs)
            self.fields['musician'].queryset = Musician.objects.filter(
                music_director_id=instance.event.music_director_id)
        else:
            super().__init__(*args, **kwargs)

    class Meta:
        model = MusicianEvent
        fields = ['instrument_for_humans', 'musician']
        # retira as labels para deixar isso por conta do front
        labels = {
            'musician': ''
        }


MusicianEventFormSetFactory = forms.inlineformset_factory(
    Event, MusicianEvent, form=MusicianEventForm,
    extra=0, can_delete=False
)


class PostEventCommentForm(forms.ModelForm):
    """
        Formulario da caixa de texto para comentarios pos eventos
    """
    class Meta:
        model = Event
        fields = ['post_event_comments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_event_comments'].widget.attrs['rows'] = 5



class AttendantsListForm(forms.ModelForm):
    """
        Formulario para fazer a estilizacao da lista de presentes
    """
    instrument_for_humans = forms.CharField(disabled=True, required=False, label='', widget=TextInput(
        attrs={'data-hide_and_show_value': 'true'}))
    musician_for_humans = forms.CharField(disabled=True, required=False, label='', widget=TextInput(
        attrs={'data-hide_and_show_value': 'true'}))

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        # instrument for humans pega o nome do instrumento traduzido e com a informacao de musico princ/sub
        # musician for humans pega so o nome do musico, e nao o valor retornado pelo __str__ do modelo
        if instance:
            if instance.musician:
                musician_name = instance.musician.name
            else:
                musician_name = '-'
            kwargs['initial'] = {'instrument_for_humans': instance.instrument_for_humans(),
                                 'musician_for_humans': musician_name}
            super().__init__(*args, **kwargs)
        else:
            super().__init__(*args, **kwargs)

        # desativa as labels deste formulario para deixar isso por conta do front
        from crispy_forms.helper import FormHelper
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # esconde o campo parent, que nao eh interessante pro usuario final
        self.fields['parent_musician_event'].widget.attrs['hidden'] = True
        # minimos e maximos da nota dos musicos
        self.fields['musician_rate'].widget.attrs['max'] = '5'
        self.fields['musician_rate'].widget.attrs['min'] = '0'

    class Meta:
        model = MusicianEvent
        fields = ['parent_musician_event', 'attended', 'musician_rate']


class AttendantsListFormset(BaseInlineFormSet):
    """
        Formset para fazer a lista de presentes
    """

    instrument_for_humans = forms.CharField(disabled=True, required=False, label='', widget=TextInput(
        attrs={'data-hide_and_show_value': 'true'}))

    def clean(self):
        parent_attended = False
        for form in self.forms:
            if form.cleaned_data:
                # se marcou que o músico estava presente e não deu a nota gera um erro de validação
                if (form.cleaned_data.get('attended') and form.cleaned_data.get('musician_rate') is None) or (
                        not form.cleaned_data.get('attended') and form.cleaned_data.get('musician_rate') is not None):
                    form.add_error(field=NON_FIELD_ERRORS,
                                   error=ValidationError(
                                       _('Please rate all the attending musicians. You cannot rate absent musicians')))
                parent_musician_event = form.cleaned_data.get('parent_musician_event')
                # se for filho
                if parent_musician_event is not None:
                    # se o pai nao foi e nem o filho, gera um erro de validação
                    if (not parent_attended and not form.cleaned_data.get('attended')) or (
                            # se o pai foi e o filho tambem, gera um erro de validação
                            parent_attended and form.cleaned_data.get('attended')):
                        form.add_error(field=NON_FIELD_ERRORS, error=ValidationError(_(
                            'Please select the attendant for each instrument! You cannot select more than one to the same instrument')))
                    # reseta a variavel que indica se o pai foi
                    parent_attended = False
                # se for pai, seta a variavel que indica se ele foi
                else:
                    parent_attended = form.cleaned_data.get('attended')


ConcludeEventFormset = forms.inlineformset_factory(
    Event, MusicianEvent,
    extra=0, can_delete=False, formset=AttendantsListFormset,
    form=AttendantsListForm,
)

# class GenricDefaultUserForm(forms.Form):
#
#     def clean(self):
#         cleaned_data = super().clean()
#         print(cleaned_data)
#         email = cleaned_data.get('email', None)
#         self_id = cleaned_data.get('id', None)
#         if self_id:
#             email_is_used = User.objects.filter(username=email).exclude(id=self_id).exists()
#         else:
#             email_is_used = User.objects.filter(username=email).exists()
#
#         if email_is_used:
#             raise ValidationError(_('This email is being used. Please enter another one.'))
