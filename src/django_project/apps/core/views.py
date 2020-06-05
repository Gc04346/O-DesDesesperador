from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from post_office import mail

from django_project.apps.core.models.base import ArtistSong, EventSong, FaqModel, Comment, has_accepted_use_terms
from .decorators import user_has_accepted_use_terms
from .forms import RawEventForm, CreateMusicianForm, UserForm, MusicianEventFormSetFactory, ArtistReferenceForm, \
    EventReferenceForm, CommentForm, UserBaseForm, ConcludeEventFormset, PostEventCommentForm
from django.utils.translation import ugettext as _

from .models import Event, Musician, MusicDirector, Artist, Producer, get_user_type, MusicianEvent, ArtistSong, \
    EventSong
from ...settings.terms_of_service import get_terms


# retorna o nivel de importancia do Faq, para fins de ordenação
def get_faq_importance(FaqModel):
    return FaqModel.importance


# retorna a data de criação do comentario
def get_date_order(Comment):
    return Comment.created_date


def faq(request):
    """
        Renders the FAQ page
    """
    context = dict()
    faqs = sorted(FaqModel.objects.all(), key=get_faq_importance)
    context['faqs'] = faqs
    return render(request, 'core/other/faq.html', context=context)


def producers_pre_register(request):
    """
        Faz o pre cadastro dos contratantes. O usuario eh criado como inativo ate que o SuperUsuario o avalie e ative
    """
    context = dict()
    if request.method == 'POST':
        form = UserBaseForm(data=request.POST)
        if form.is_valid():
            try:
                if not form.cleaned_data['password']:
                    raise FieldError
                user = User.objects.create(username=form.cleaned_data['email'], email=form.cleaned_data['email'],
                                           first_name=form.cleaned_data['name'], is_active=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                Producer.objects.create(
                    user_id=user.id,
                    phone=form.cleaned_data['phone'],
                    whatsapp=form.cleaned_data['whatsapp'],
                    address=form.cleaned_data['address'],
                    cep=form.cleaned_data['cep'],
                    doc_number=form.cleaned_data['doc_number'],
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                )
                messages.success(request, _(
                    'Your profile has been submitted successfully! Our team will analyse it and you will receive an email if it is approved.'),
                                 extra_tags='alert')
            except FieldError:
                messages.warning(request, _('Password field is mandatory.'), extra_tags='alert')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='alert')
    else:
        form = UserBaseForm()
    context['form'] = form
    return render(request, 'core/other/pre_register.html', context=context)


@login_required
@staff_member_required
def activate_user(request, user_id):
    """
        O SuperUsuario deve ativar usuarios de contratantes feitos atraves do pre-cadastro.
        Esta view eh ligada no admin do Produtor
    """
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    send_mail_user_active(user.email, request)
    # redirecionando especificamente de volta para a pagina de edicao daquele produtor no admin
    # a funcao recebe como parametro uma string, e esta string eh prenchida com dados informados pelo format
    return HttpResponseRedirect(
        '{}producer/{}/change/'.format(request.build_absolute_uri(reverse('admin:app_list', args=('core',))),
                                       Producer.objects.get(user=user).id))


# ----------------------------
# MAIN views - comuns a todos
# ----------------------------
@login_required
def accept_terms(request):
    """
        Aceita os termos e condicoes de uso
    """
    user_type = get_user_type(request.user)
    user = User.objects.get(id=request.user.id)
    try:
        if user_type == 'artist':
            Artist.objects.get(user=user).accept_use_terms()
        if user_type == 'producer':
            Producer.objects.get(user=user).accept_use_terms()
        if user_type == 'musician':
            Musician.objects.get(user=user).accept_use_terms()
        if user_type == 'music_director':
            MusicDirector.objects.get(user=user).accept_use_terms()
    except ObjectDoesNotExist as e:
        return HttpResponse(e)
    return redirect('core:homepage')


@login_required
def homepage(request):
    """
        Renders the homepage
    """
    context = dict()
    user_type = get_user_type(request.user)
    context['user_type'] = user_type
    context['terms'] = get_terms(user_type)
    # exibe o modal de termos de uso caso o usuario ainda nao tenha aceito
    context['has_not_accepted_use_terms'] = not has_accepted_use_terms(request.user.id)
    # o conteudo do contexto varia para cada user type
    if user_type == 'artist':
        context['events'] = Event.objects.filter(
            Q(artist__user_id=request.user.id) | Q(producer__user_id=request.user.id))
        context['self'] = Artist.objects.get(user_id=request.user.id)
    elif user_type == 'producer':
        context['events'] = Event.objects.filter(producer__user_id=request.user.id)
        context['self'] = Producer.objects.get(user_id=request.user.id)
    elif user_type == 'music_director':
        music_director = MusicDirector.objects.get(user_id=request.user.id)
        context['events'] = music_director.event_set.all()
        context['musicians'] = music_director.musician_set.all()
        context['self'] = MusicDirector.objects.get(user_id=request.user.id)
    elif user_type == 'musician':
        # musician = Musician.objects.get(user_id=request.user.id)
        # musician_events = musician.musicianevent_set.prefetch_related().all()
        musician_events = MusicianEvent.objects.filter(musician__user_id=request.user.id).prefetch_related()
        context['musician_events'] = musician_events
        events = []
        for musician_event in musician_events:
            events.append(musician_event.event)
        context['events'] = events
        context['self'] = Musician.objects.get(user_id=request.user.id)

    # as particularidades de cada usuario no template sao tratadas dentro do mesmo
    return render(request, 'core/other/loggedhomepage.html', context=context)


@login_required
@user_has_accepted_use_terms
def profile(request):
    """
        Renders the profile template
    """
    user_type = get_user_type(request.user)
    if request.method == 'POST':
        # artistas tem que ver um template um pouco diferente, por causa da aceitacao de musicos
        is_artist = False
        if user_type == 'artist':
            is_artist = True
        form = UserForm(is_artist=(user_type == 'artist'), data=request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            # user.email = form.cleaned_data['email']
            # user.username = form.cleaned_data['email']
            # user.first_name = form.cleaned_data['name']
            from django_project.apps.core.models.base import set_user_attribute
            set_user_attribute(request.user, 'email', form.cleaned_data['email'])
            set_user_attribute(request.user, 'name', form.cleaned_data['name'])
            set_user_attribute(request.user, 'phone', form.cleaned_data['phone'])
            set_user_attribute(request.user, 'address', form.cleaned_data['address'])
            set_user_attribute(request.user, 'cep', form.cleaned_data['cep'])
            set_user_attribute(request.user, 'doc_number', form.cleaned_data['doc_number'])

            if user_type == 'artist':
                set_user_attribute(request.user, 'phone', form.cleaned_data['phone'])
                set_user_attribute(request.user, 'accept_v', form.cleaned_data['accept_v'])
                set_user_attribute(request.user, 'accept_g', form.cleaned_data['accept_g'])
                set_user_attribute(request.user, 'accept_b', form.cleaned_data['accept_b'])
                set_user_attribute(request.user, 'accept_t', form.cleaned_data['accept_t'])
                set_user_attribute(request.user, 'accept_bt', form.cleaned_data['accept_bt'])
                set_user_attribute(request.user, 'accept_bvt', form.cleaned_data['accept_bvt'])
                set_user_attribute(request.user, 'accept_bvs', form.cleaned_data['accept_bvs'])
                set_user_attribute(request.user, 'accept_bvc', form.cleaned_data['accept_bvc'])

            if form.cleaned_data['password'] and form.cleaned_data['password'] != '':
                user.set_password(form.cleaned_data['password'])
            messages.success(request, _('Your profile has been updated successfully!'), extra_tags='alert')
            user.save()
    else:
        from django_project.apps.core.models.base import get_user_attribute
        # from django.http import HttpResponse
        if request.user.is_authenticated:
            initial = dict(
                user_id=request.user.id,
                email=request.user.get_username(),
                name=request.user.get_full_name(),
                whatsapp=get_user_attribute(request.user, 'whatsapp'),
                phone=get_user_attribute(request.user, 'phone'),
                address=get_user_attribute(request.user, 'address'),
                cep=get_user_attribute(request.user, 'cep'),
                doc_number=get_user_attribute(request.user, 'doc_number'),
                # password='',
                # password_confirmation='',
            )
            is_artist = False
            if user_type == 'artist':
                is_artist = True
                artist = Artist.objects.get(user_id=request.user.id)
                initial['accept_v'] = artist.accept_v
                initial['accept_g'] = artist.accept_g
                initial['accept_b'] = artist.accept_b
                initial['accept_t'] = artist.accept_t
                initial['accept_bt'] = artist.accept_bt
                initial['accept_bvt'] = artist.accept_bvt
                initial['accept_bvs'] = artist.accept_bvs
                initial['accept_bvc'] = artist.accept_bvc
            form = UserForm(initial=initial, is_artist=is_artist)
        else:
            return HttpResponseNotFound
        # music_director = MusicDirector.objects.get(user_id=request.user.id)
        # musician_id = request.GET.get('musician_id', None)
        # if musician_id:
    context = dict()
    context['form'] = form
    context['user_type'] = user_type
    return render(request, 'core/other/profle.html', context=context)


@login_required
@user_has_accepted_use_terms
def event(request, event_id):
    """
        Renders the event details page
    """
    user_type = get_user_type(request.user)
    try:
        from django.db.models import Q
        user_id = request.user.id
        # pega o evento em questao, sem permitir que usuarios que nao pertencem àquele evento o visualizem
        event = Event.objects.filter(Q(id=event_id) & (
                Q(artist__user_id=user_id) | Q(music_director__user_id=user_id) | Q(
            musicianevent__musician__user_id=user_id) | Q(
            producer__user_id=user_id))).first()
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    music_director = event.music_director
    context = dict()
    context['user_type'] = user_type
    context['user'] = request.user
    context['event'] = event
    context['music_director'] = music_director
    # a construcao do contexto varia de acordo com o tipo de usuario
    if user_type == 'music_director':
        # pending confirmation vai controlar o botao de add musicos ao evento na view. se todos ja tiverem confirmado,
        # o botao some
        context['pending_confirmation'] = False
        for musician_event in MusicianEvent.objects.filter(event=event):
            # se achar algum musico pendente confirmacao, nao precisa iterar pelo resto. o botao ja tem que aparecer
            if not musician_event.confirmation:
                context['pending_confirmation'] = True
                break
        context['musician_events'] = MusicianEvent.objects.filter(event=event)
        context['artist_songs'] = ArtistSong.objects.filter(artist_id=event.artist.id)
        context['event_songs'] = EventSong.objects.filter(event_id=event.id)
        comments = sorted(Comment.objects.filter(event=event), key=get_date_order, reverse=False)
        context['comments'] = comments
    elif user_type == 'artist':
        comments = sorted(Comment.objects.filter(event=event), key=get_date_order, reverse=False)
        context['comments'] = comments
        # nao necessariamente o artista, agindo como contratante, sera o artista daquele evento
        context['artist_is_producer'] = event.producer.user_id == request.user.id
        context['artist_is_event_artist'] = event.artist.user_id == request.user.id
    elif user_type == 'musician':
        context['musician_events'] = MusicianEvent.objects.get(event=event, musician__user_id=request.user.id)
        context['songs'] = EventSong.objects.filter(event_id=event.id)
    else:  # so pra garantir que pros outros usuarios nao vai dar pau
        context['musician_events'] = 0
    return render(request, 'core/event/event.html', context=context)


@login_required
@user_has_accepted_use_terms
def pastevents(request):
    """
        Renders the past events list
    """
    context = dict()
    user_type = get_user_type(request.user)
    context['user_type'] = user_type
    # as queries nao permitem que usuarios que nao estejam nos eventos os visualizem
    if user_type == 'artist':
        context['events'] = Event.objects.filter(
            Q(artist__user_id=request.user.id) | Q(producer__user_id=request.user.id))
    elif user_type == 'music_director':
        context['events'] = Event.objects.filter(music_director__user_id=request.user.id)
    elif user_type == 'producer':
        context['events'] = Event.objects.filter(producer__user_id=request.user.id)
    elif user_type == 'musician':
        # musician = Musician.objects.get(user_id=request.user.id)
        # musician_events = musician.musicianevent_set.prefetch_related().all()
        musician_events = MusicianEvent.objects.filter(musician__user_id=request.user.id).prefetch_related()
        context['musician_events'] = musician_events
        events = []
        for musician_event in musician_events:
            events.append(musician_event.event)
        context['events'] = events
    return render(request, 'core/event/pastevents.html', context=context)


# ----------------------------
# Views do Music Director
# ----------------------------
@login_required
@user_has_accepted_use_terms
def musicians_list(request):
    """
        Lista os musicos do diretor musical
    """
    user_type = get_user_type(request.user)

    # somente diretores musicais podem ter acesso a essa pagina
    if user_type != 'music_director':
        return HttpResponseForbidden()
    else:
        context = dict()
        try:
            # garantindo que eu pegue apenas os musicos daquele diretor musical
            context['musicians'] = Musician.objects.filter(music_director__user_id=request.user.id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound
        context['user_type'] = user_type
        context['self'] = MusicDirector.objects.get(user_id=request.user.id)
        return render(request, 'core/musicdirector/musicianslist.html', context=context)


@login_required
@user_has_accepted_use_terms
def create_or_edit_musician(request):
    """
        Criar ou editar os musicos do dm
    """
    # somente diretores musicais tem acesso a esta pagina
    if get_user_type(request.user) != 'music_director':
        return HttpResponseForbidden()
    context = dict()
    if request.method == 'POST':
        form = CreateMusicianForm(request.POST)
        if form.is_valid():
            try:
                # este metodo static eh responsavel por criar/atualizar o objeto
                musician = Musician.set_musician_and_user(form=form.cleaned_data)
                from django.urls import reverse
                messages.success(request, _('Musician created/updated successfully!'), extra_tags='alert')
                return redirect('{}?musician_id={}'.format(reverse('core:musicianmanagement'), musician.id))
            except FieldError:
                return HttpResponseBadRequest()
    else:
        try:
            music_director = MusicDirector.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound
        musician_id = request.GET.get('musician_id', None)
        if musician_id:
            try:
                musician = Musician.objects.get(id=musician_id, music_director=music_director)
                context['musician_id'] = musician_id
            except ObjectDoesNotExist:
                return HttpResponseNotFound

            form = CreateMusicianForm(initial=dict(
                music_director_id=musician.music_director.id,
                musician_id=musician.id,
                name=musician.user.first_name,
                phone=musician.phone,
                whatsapp=musician.whatsapp,
                instrument=musician.instrument,
                email=musician.user.email,
            ))
            pass
        else:
            form = CreateMusicianForm(initial=dict(music_director_id=music_director.id))

    context['form'] = form
    context['user_type'] = get_user_type(request.user)
    return render(request, 'core/musicdirector/createoreditmusician.html', context=context)


@login_required
@user_has_accepted_use_terms
def delete_musician(request, musician_id):
    """
        Deletar musicos do dm
    """
    if get_user_type(request.user) != 'music_director':
        return HttpResponseForbidden()
    try:
        # somente o diretor daquele musico pode deleta-lo
        musician = Musician.objects.get(id=musician_id, music_director__user_id=request.user.id)
        user = User.objects.get(id=musician.user.id)
        musician.delete()
        user.delete()
        messages.warning(request, _('Musician deleted!'), extra_tags='alert')
    except ObjectDoesNotExist:
        return HttpResponseNotFound
    return redirect('core:musicianslist')


@login_required
@user_has_accepted_use_terms
def add_musicians(request, event_id):
    """
        add musicos a determinado evento. NAO eh a view de CRIAR musicos.
    """
    if get_user_type(request.user) != 'music_director':
        return HttpResponseForbidden()
    try:
        # garantindo que retorne apenas os eventos daquele determinado dm
        music_director = MusicDirector.objects.get(user_id=request.user.id)
        event = Event.objects.get(id=event_id, music_director=music_director)
    except ObjectDoesNotExist:
        return HttpResponseNotFound

    if request.method == 'POST':
        formset = MusicianEventFormSetFactory(request.POST, instance=event)
        if formset.is_valid():
            formset.save()
            messages.success(request, _('Musician added to event! Pending his or her confirmation...'),
                             extra_tags='alert')
            return redirect('core:event', event.id)
    else:
        formset = MusicianEventFormSetFactory(instance=event)
    context = dict()
    context['event'] = Event.objects.get(id=event_id)
    context['formset'] = formset
    context['user_type'] = get_user_type(request.user)
    return render(request, 'core/musicdirector/addmusicians.html', context=context)


@login_required
@user_has_accepted_use_terms
def set_references_for_musicians(request, event_id):
    """
        Definir as referencias do artista para os musicos naquele evento
    """
    if get_user_type(request.user) != 'music_director':
        return HttpResponseForbidden()
    context = dict()
    event = Event.objects.get(id=event_id)
    context['event'] = event
    if request.method == 'POST':
        form = EventReferenceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.setEvent(event)
                EventSong.set_song_and_artist(form=form.cleaned_data)
                from django.urls import reverse
                messages.success(request, _('Song uploaded successfully!'), extra_tags='alert')
                return redirect('core:event', event.id)
            except FieldError:
                return HttpResponseBadRequest()
    else:
        song_id = request.GET.get('event_song_id', None)
        if song_id:
            try:
                song = EventSong.objects.get(id=song_id, event_id=event.id)
                context['song_id'] = song.id
            except ObjectDoesNotExist:
                return HttpResponseNotFound

            form = EventReferenceForm(initial=dict(
                reference_id=song_id,
                event_id=event.id,
                name=song.name,
                file=song.file,
                notes=song.notes,
                links=song.links,
            ))
            pass
        else:
            form = EventReferenceForm(initial=dict(artist_id=event.id))

    context['form'] = form
    context['user_type'] = get_user_type(request.user)
    return render(request, 'core/artist/managesongs.html', context=context)


# ----------------------------
# Views do Artista
# ----------------------------
@login_required
@user_has_accepted_use_terms
def my_songs(request):
    """
        pagina de listagem das referencias do artista pros diretores musicais
    """
    # somente artistas tem acesso a esta pagina
    if get_user_type(request.user) != 'artist':
        return HttpResponseForbidden()
    try:
        songs = ArtistSong.objects.filter(artist__user_id=request.user.id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound
    context = dict()
    context['songs'] = songs
    context['user_type'] = get_user_type(request.user)
    return render(request, 'core/artist/mysongs.html', context=context)


@login_required
@user_has_accepted_use_terms
def manage_songs(request):
    """
        add/editar referencia do artista pros diretores
    """
    if get_user_type(request.user) != 'artist':
        return HttpResponseForbidden()
    context = dict()
    if request.method == 'POST':
        form = ArtistReferenceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.setArtist(request.user)
                ArtistSong.set_song_and_artist(form=form.cleaned_data)
                from django.urls import reverse
                messages.success(request, _('Song uploaded successfully!'), extra_tags='alert')
                return redirect('core:my_songs')
            except FieldError:
                return HttpResponseBadRequest()
    else:
        song_id = request.GET.get('song_id', None)
        if song_id:
            try:
                song = ArtistSong.objects.get(id=song_id, artist__user_id=request.user.id)
                context['song_id'] = song.id
            except ObjectDoesNotExist:
                return HttpResponseNotFound
            form = ArtistReferenceForm(initial=dict(
                reference_id=song_id,
                artist_id=request.user.artist.id,
                name=song.name,
                file=song.file,
                notes=song.notes,
                links=song.links,
            ))
        else:
            form = ArtistReferenceForm(initial=dict(artist_id=request.user.artist.id))

    context['form'] = form
    context['user_type'] = get_user_type(request.user)
    return render(request, 'core/artist/managesongs.html', context=context)


# ----------------------------
# Views do contratante
# ----------------------------
@login_required
@user_has_accepted_use_terms
def new_event(request):
    """
        Renders the event creation page
    """
    # somente contratantes podem criar novos eventos
    if get_user_type(request.user) != 'producer' and get_user_type(request.user) != 'artist':
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = RawEventForm(request.POST)
        if form.is_valid():
            # metodo definido no form para definir o campo de produtor no cleaned data
            form.setProducer(request.user)
            try:
                # cria o objeto evento e os respectivos musician events sem musico
                event = Event.create_event_and_musician_event(form=form.cleaned_data)
                send_mail_new_event(event, request)
                messages.success(request, _('Event created successfully! Pending confirmation from the music director '
                                            'and the artist you chose...'), extra_tags='success')
                # seta as variaveis de preco do evento
                event.event_price_calculator()
                return redirect('core:event', event.id)
            except FieldError:
                return FieldError
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        form = RawEventForm()

    context = dict()
    context['form'] = form
    # so o producer tem acesso a esta view, entao da pra economizar processamento atribuindo producer direto
    context['user_type'] = 'producer'
    return render(request, 'core/event/newevent.html', context=context)


@login_required
@user_has_accepted_use_terms
def event_paid(request, event_id):
    """
        Envia os emails de notificacao e seta os atributos de evento quando o contratante pagar
    """
    # todo setar os atributos payment_date, invoice_number e paid_ammount no evento
    send_mail_event_paid(Event.objects.get(id=event_id), request)
    # todo NETO validar se eh isso msm


@login_required
@user_has_accepted_use_terms
def event_cancelled(request, event_id):
    """
        Quando um evento eh cancelado, is_active recebe False. Ele nao eh deletado do banco de dados
    """
    if request.method == 'POST':
        try:  # garantindo que quem tá querendo deletar o evento eh o contratante daquele evento
            event = Event.objects.get(id=event_id, producer__user_id=request.user.id)
            # o evento so pode ser deletado se nao tiver artista OU nao tiver dm OU algum dos dois ainda nao tenha confirmado
            if not event.artist or not event.music_director or event.confirmed != 'YES' or event.artist_confirmation != 'YES':
                send_mail_event_cancelled(event)
                event.is_active = False
                event.save()
            else:
                messages.warning(request, _('This event cannot be deleted!'), extra_tags='alert')
                return redirect('core:event', event_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound
        messages.warning(request, _('Event cancelled!'), extra_tags='alert')
        return redirect('core:homepage')
    # nao eh permitido acessar essa pagina como metodo get
    return HttpResponseForbidden()


@login_required
@user_has_accepted_use_terms
def conclude_event(request, event_id):
    """
    View responsavel por fazer com que o produtor:
        1. faca a lista de presenca
        2. avalie os musicos
        3. comente sobre o evento
    Quando isso tudo for feito, o sistema ira:
        1. marcar o evento como finalizado
        2. distribuir o pagamento
        3. calcular e setar rate do dm
        4. marcar que o pagamento foi distribuido
    """
    context = dict()
    event = Event.objects.get(id=event_id)
    # o contratante so pode acessar a pagina se o evento ja tiver sido totalmente pago
    if not event.paid_ammount or event.total_price() < event.paid_ammount:
        messages.error(request, _('You must pay the full price for the event before concluding it!'),
                       extra_tags='error')
        return redirect('core:event', event.id)
    if request.method == 'POST':
        formset = ConcludeEventFormset(request.POST, instance=event)
        form = PostEventCommentForm(request.POST, instance=event)
        if formset.is_valid() and form.is_valid():
            formset.save()
            form.save()
            # faz distribuicao de pagamentos e define as variaveis necessarias para a finalizacao
            event.conclude_event()
            messages.success(request, _('Event finalized'),
                             extra_tags='alert')
            send_mail_event_finalized(event)
            send_mail_musicians_rated(event)
            return redirect('core:event', event.id)
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        formset = ConcludeEventFormset(instance=event)
        form = PostEventCommentForm(instance=event)
    context['formset'] = formset
    context['form'] = form
    context['event'] = event
    return render(request, 'core/event/concludeevent.html', context=context)


# ----------------------------
# Views do Musico
# ----------------------------
@login_required
@user_has_accepted_use_terms
def add_musicians_confirmation(request, musician_event_id):
    """
        Musico confirmou presenca no evento
    """
    if get_user_type(request.user) != 'musician':
        return HttpResponseForbidden()
    if request.method == 'POST':
        try:
            musician_event = MusicianEvent.objects.get(id=musician_event_id, musician__user_id=request.user.id)
            musician_event.confirmation = Event.get_confirmed_status_code()
            musician_event.save()
            send_mail_musician_confirmation_or_refusal(Event.objects.get(id=musician_event.event_id), True, request)  # Confirmation mail
            messages.success(request, _('You have confirmed your presence in this event!'), extra_tags='alert')
        except (ObjectDoesNotExist, FieldError):
            return HttpResponseNotFound

        return redirect('core:event', event_id=musician_event.event.id)

    # nao eh permitido acessar essa pagina como metodo get
    return HttpResponseForbidden()


@login_required
@user_has_accepted_use_terms
def add_musicians_refusal(request, musician_event_id):
    """
        Musico recusou participar no evento
    """
    if get_user_type(request.user) != 'musician':
        return HttpResponseForbidden()
    if request.method == 'POST':
        try:
            musician_event = MusicianEvent.objects.get(id=musician_event_id, musician__user_id=request.user.id)
            musician_event.confirmation = Event.get_refused_status_code()
            musician_event.save()
            send_mail_musician_confirmation_or_refusal(Event.objects.get(id=musician_event.event_id), False, request)  # Non-Acceptance Email
            messages.warning(request, _('You have refused to play in the event!'), extra_tags='alert')
        except ObjectDoesNotExist:
            return HttpResponseNotFound
        return redirect('core:homepage')

    # nao eh permitido acessar essa pagina como metodo get
    return HttpResponseForbidden()


# ----------------------------
# Views do Artista/ Music Director
# ----------------------------
@login_required
@user_has_accepted_use_terms
def song_delete(request, song_id):
    """
        deletar a referencia. tanto do artista pro dm quanto do dm pros musicos
    """
    user_type = get_user_type(request.user)
    if user_type != 'artist' and user_type != 'music_director':
        return HttpResponseForbidden()
    try:
        # garante que quem esta tentando deletar a musica eh o dono dela
        if user_type == 'artist':
            song = ArtistSong.objects.get(id=song_id, artist__user_id=request.user.id)
            song.delete()
            messages.warning(request, _('Song has been deleted!'), extra_tags='alert')
            return redirect('core:my_songs')
        elif user_type == 'music_director':
            song = EventSong.objects.get(id=song_id)
            song.delete()
            messages.warning(request, _('Song has been deleted!'), extra_tags='alert')
            return redirect('core:homepage')
    except ObjectDoesNotExist:
        return HttpResponseNotFound


@login_required
@user_has_accepted_use_terms
def send_message(request, event_id):
    """
        troca de mensagens entre o diretor e o artista
    """
    context = dict()
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.set_data(request.user, event)
            Comment.set_new_comment(form.cleaned_data)
    else:
        form = CommentForm()
    context['form'] = form
    return redirect('core:event', event.id)


@login_required
@user_has_accepted_use_terms
def delete_message(request, comment_id, event_id):
    """
        deleta a mensagem artista/dm
    """
    try:
        comment = Comment.objects.get(id=comment_id, author_id=request.user.id)
        comment.delete()
    except ObjectDoesNotExist:
        return HttpResponseNotFound
    return redirect('core:event', event_id)


@login_required
@user_has_accepted_use_terms
def event_confirmed(request, event_id):
    """
        artista ou dm confirmou presenca no evento
    """
    user = request.user
    user_type = get_user_type(user)
    if request.method == 'POST':
        try:
            if user_type == 'artist':
                event = Event.objects.get(id=event_id, artist__user_id=request.user.id)
                event.artist_confirmation = Event.get_confirmed_status_code()
                send_mail_artist_or_dm_confirm_or_refuse_participation(request, event, True)  # Confirmation mail
                event.save()
            elif user_type == 'music_director':
                event = Event.objects.filter(id=event_id, music_director__user_id=user.id).first()
                musician_events = MusicianEvent.objects.filter(event_id=event.id)
                # dm so pode confirmar participacao depois de atribuir completamente a banda
                for musician_event in musician_events:
                    if not musician_event.musician:
                        messages.warning(request, _(
                            'You must assign a whole band before you can confirm your participation in this event!'),
                                         extra_tags='alert')
                        return redirect('core:event', event_id)
                event.confirmed = Event.get_confirmed_status_code()
                send_mail_artist_or_dm_confirm_or_refuse_participation(request, event, True)  # Confirmation mail
                event.save()
            messages.success(request, _('You have confirmed your participation in this event!'), extra_tags='alert')
            return redirect('core:event', event_id)
        # pode ocorrer erro tanto na obtencao do objeto quanto na hora de modificar seu atributo
        except (ObjectDoesNotExist, FieldError, ):
            return HttpResponseNotFound()

    # nao eh permitido acessar essa pagina como metodo get
    return HttpResponseForbidden()


@login_required
@user_has_accepted_use_terms
def event_refused(request, event_id):
    """
        artista ou dm recusou participar no evento
    """
    try:
        if get_user_type(request.user) == 'artist':
            event = Event.objects.get(id=event_id, artist__user_id=request.user.id)
            event.artist_confirmation = Event.get_refused_status_code()
            send_mail_artist_or_dm_confirm_or_refuse_participation(request, event, False)  # refusal mail
            event.save()
            messages.warning(request, _('Event refused!'), extra_tags='alert')
        elif get_user_type(request.user) == 'music_director':
            event = Event.objects.get(id=event_id, music_director__user_id=request.user.id)
            event.confirmed = Event.get_refused_status_code()
            send_mail_artist_or_dm_confirm_or_refuse_participation(request, event, False)  # refusal mail
            event.save()
            messages.warning(request, _('Event refused!'), extra_tags='alert')
        else:  # somente dms e artistas tem acesso a esta pagina
            return HttpResponseForbidden()
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    return redirect('core:homepage')


# ----------------------------
# Metodos de envio de email
# ----------------------------

def send_mail_event_paid(event, request):
    """
        envia email para artista e dm quando o contratante pagar pelo evento
    """
    try:
        mail.send(
            [event.music_director.user.email, event.artist.user.email],
            subject='{} {} {}.'.format(_('The event'), event.name, _('has been paid by the producer')),
            html_message='{}.<br > {} <a href="{}">{}</a> {}.'.format(
                _(
                    'The producer has paid for the event. You can now safely confirm your presence, we will make sure the payment is distributed properly after the event is concluded.'),
                _('Click'), request.build_absolute_uri(reverse('core:event', kwargs={'event_id': event.id})), _('here'),
                _('to go to the event page.')),
        )
    except Exception:
        pass


def send_mail_event_finalized(event):
    """
        envia email pro artista e dm quando o contratante finalizar o evento
    """
    recipients = []
    try:
        recipients.append(event.artist.user.email)
        recipients.append(event.music_director.user.email)
        for musician_event in MusicianEvent.objects.filter(event=event):
            recipients.append(musician_event.musician.user.email)
    except Exception:
        pass
    if len(recipients) > 0:
        mail.send(
            recipients,
            subject='{} {} {}.'.format(_('The event'), event.name, _('has been concluded by the producer')),
            html_message='{} {} {}. {}'.format(_('The event'), event.name, _('has been concluded by the producer'),
                                               _('Thank you for your participation!'))
        )


def send_mail_musicians_rated(event):
    """
        envia email para os musicos quando eles forem avaliados
    """
    for musician_event in MusicianEvent.objects.filter(event=event):
        try:
            mail.send(
                [musician_event.musician.user.email],
                subject='{} {} {}'.format(_('Your performance on'), event.name, _('has been rated!')),
                html_message='{} {} {} {} {}. {}!'.format(_('You have received'), musician_event.musician_rate, _('stars'),
                                                          _('for your performance on'), event.name, _('congratulations'))
            )
        except Exception:
            pass


def send_mail_new_event(event, request):
    """
        envia emails para o artista e o diretor musical quando um novo evento eh criado
    """
    try:
        recipients = [event.artist.user.email, event.music_director.user.email]
    except Exception:
        recipients = None
    if recipients:
        mail.send(
            recipients,
            subject='{}'.format(_('New event 2 u!')),
            html_message='{}.<br > {} <a href="{}">{}</a> {}.'.format(
                _('You have been added to a new event'), _('Click'),
                request.build_absolute_uri(reverse('core:event', kwargs={'event_id': event.id})), _('here'), _('to see')),
        )


def send_mail_event_cancelled(event):
    """
        envia emails para o artista, diretor musical e musicos quando evento eh cancelado
    """
    recipients = []
    for musician_event in MusicianEvent.objects.filter(event=event, musician__isnull=False,
                                                       confirmation=Event.get_confirmed_status_code()):
        try:
            recipients.append(musician_event.musician.user.email)
        except Exception:
            pass

    # se o evento tiver artista e diretor
    if event.artist and event.music_director:
        try:
            recipients.append(event.artist.user.email)
            recipients.append(event.music_director.user.email)
        except Exception:
            pass
    # se o evento so tiver diretor
    elif not event.artist and event.music_director:
        try:
            recipients.append(event.music_director.user.email)
        except Exception:
            pass
    # se o evento so tiver artista
    elif event.artist and not event.music_director:
        try:
            recipients.append(event.artist.user.email)
        except Exception:
            pass
    if len(recipients) > 0:
        mail.send(
            recipients,
            subject='{}'.format(_('Event cancelled!')),
            html_message='{} {} {}'.format(
                _('The event'), event.name, _('that you were participating on was just cancelled!'), )
        )


def send_mail_artist_or_dm_confirm_or_refuse_participation(request, event, confirm):
    """
        envia emails para o contratante quando o artista ou diretor musical confirmam ou rejeitam presenca
    """
    try:
        recipient = event.producer.user.email
    except Exception:
        recipient = None
    if recipient:
        if confirm:  # Evento confirmado
            mail.send(
                recipient,
                subject='{}'.format(_('Event confirmed !!')),
                html_message='{}.<br > {} <a href="{}">{}</a> {}.'.format(
                    _('You have a new member in event'), _('Click'),
                    request.build_absolute_uri(reverse('core:event', kwargs={'event_id': event.id})), _('here'),
                    _('to see'))
            )
        else:
            mail.send(
                recipient,
                subject='{}'.format(_('Participation in event refused !!')),
                html_message='{}.<br > {} <a href="{}">{}</a> {}.'.format(
                    _('One member did not accept to participate in your event'), _('Click'),
                    request.build_absolute_uri(reverse('core:event', kwargs={'event_id': event.id})), _('here'),
                    _('to see'))
            )


def send_mail_musician_confirmation_or_refusal(event, accept, request):
    """
        envia emails para o diretor musical quando um musico confirma ou rejeita participacao no evento
    """
    try:
        recipient = event.music_director.user.email
    except Exception:
        recipient = None
    if recipient:
        if accept:  # Show aceito.
            mail.send(
                recipient,
                subject='{}'.format(_('Event accepted !!')),
                html_message='{}.<br > {} <a href="{}">{}</a> {}.'.format(
                    _('One musician has accepted to participate in an event'), _('Click'),
                    request.build_absolute_uri(reverse('core:event', kwargs={'event_id': event.id})), _('here'),
                    _('to see'))
            )
        else:
            mail.send(
                recipient,
                subject='{}'.format(_('Event not accepted !!')),
                html_message='{}.<br > {} <a href="{}">{}</a> {}.'.format(
                    _('One musician has refused to participate in an event'), _('Click'),
                    request.build_absolute_uri(reverse('core:event', kwargs={'event_id': event.id})), _('here'),
                    _('to see'))
            )


def send_mail_new_user(user_email, request):
    """
        envia emails quando novos usuarios sao criados com o email passado como parametro
    """

    mail.send(
        user_email,
        subject='{}'.format(_('Welcome to Gig2You!')),
        html_message='{}.<br > {} <a href="{}">{}</a> {}. <br><br><br>{}.'.format(
            _('Welcome to the Gig2You platform! We hope you have a nice time around here =).'), _('Click'),
            request.build_absolute_uri(reverse('password_reset')), _('here'),
            _('to set your password and finish your registry'),
            _('If you have received this email by mistake, simply ignore it. We are sorry for the inconvenience')),
    )


def send_mail_user_active(user_email, request):
    """
        envia emails quando o perfil do produtor for ativado
    """

    mail.send(
        user_email,
        subject='{}'.format(_('Welcome to Gig2You!')),
        html_message='{}.<br > {} <br> {} <a href="{}">{}</a> {}. <br><br><br>{}.'.format(
            _('Welcome to the Gig2You platform! We hope you have a nice time around here =).'),
            _('Your profile has been activated! Now you can log in and use all the features of our platform!'),
            _('Click'), request.build_absolute_uri(reverse('core:homepage')), _('here'),
            _('to log in!'),
            _('If you have received this email by mistake, simply ignore it. We are sorry for the inconvenience')),
    )
