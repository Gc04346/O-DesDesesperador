from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST

from theundesperator.apps.ceremony.forms import GuestFrontForm, CategoryFrontForm, ProviderFrontForm, CeremonyFrontForm, \
    ClothesPlannerFrontForm, OccasionFrontForm, MusicFrontForm, GroomsmanFrontForm
from theundesperator.apps.ceremony.models import Guest, Category, Provider, Ceremony, ClothesPlanner, Occasion, Music, \
    Groomsman


def guest_create(request):
    context = dict()
    if request.method == 'POST':
        form = GuestFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('{} was added to the guest list!').format(form.cleaned_data["name"]),
                             extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    form = GuestFrontForm()
    guests_ammount = Guest.objects.all().count()
    context['form'] = form
    context['guests_ammount'] = guests_ammount
    return render(request, 'guests/index.html', context=context)


def guests_list(request):
    context = dict()
    guests = Guest.objects.all()
    context['guests'] = guests
    context['guest_groups'] = Guest.get_all_guest_groups()
    return render(request, 'guests/list.html', context=context)


@require_POST
def guest_update(request, guest_id):
    guest = Guest.objects.get(id=guest_id)
    form = GuestFrontForm(data=request.POST, files=request.FILES, instance=guest)
    response = dict()
    form_is_valid = form.is_valid()
    if form_is_valid:
        form.save()
        messages.success(request, _('{} was updated!').format(form.cleaned_data["name"]), extra_tags='success')
        response['status'] = 'success'
    else:
        messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
        response['status'] = 'error'
        response['data'] = form_is_valid
    return JsonResponse(response)


def guest_delete(request, guest_id):
    response = dict()
    Guest.objects.get(id=guest_id).delete()
    response['status'] = 'success'
    return JsonResponse(response)


def groomsman_create(request):
    context = dict()
    if request.method == 'POST':
        form = GroomsmanFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            groomsman = form.save()
            if groomsman.duo:
                g_duo = Groomsman.objects.get(id=groomsman.duo_id)
                g_duo.duo = groomsman
                g_duo.save()
            messages.success(request, _('{} was added to the groomsmen list!').format(form.cleaned_data["name"]),
                             extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    form = GroomsmanFrontForm()
    solo_groomsmen_ammount = Groomsman.objects.filter(duo__isnull=True).count()
    duo_groomsmen_ammount = int(Groomsman.objects.filter(duo__isnull=False).count() // 2)
    errors = False
    if Groomsman.objects.all().count() % 2 == 0 and solo_groomsmen_ammount % 2 != 0:
        errors = True
    context['form'] = form
    context['consistency_errors'] = errors
    context['solo_groomsmen_ammount'] = solo_groomsmen_ammount
    context['duo_groomsmen_ammount'] = duo_groomsmen_ammount
    return render(request, 'groomsmen/index.html', context=context)


def groomsman_list(request):
    context = dict()
    groomsmen = Groomsman.objects.all()
    solo_groomsmen_ammount = Groomsman.objects.filter(duo__isnull=True).count()
    duo_groomsmen_ammount = int(Groomsman.objects.filter(duo__isnull=False).count() // 2)
    errors = False
    if Groomsman.objects.all().count() % 2 == 0 and solo_groomsmen_ammount % 2 != 0:
        errors = True
    context['groomsmen'] = groomsmen
    context['consistency_errors'] = errors
    context['solo_groomsmen_ammount'] = solo_groomsmen_ammount
    context['duo_groomsmen_ammount'] = duo_groomsmen_ammount
    return render(request, 'groomsmen/list.html', context=context)


def groomsman_update(request, groomsman_id):
    context = dict()
    groomsman = Groomsman.objects.get(id=groomsman_id)
    if request.method == 'POST':
        form = GroomsmanFrontForm(data=request.POST, files=request.FILES, instance=groomsman)
        form_is_valid = form.is_valid()
        if form_is_valid:
            groomsman = form.save()
            if groomsman.duo:
                g_duo = Groomsman.objects.get(id=groomsman.duo_id)
                g_duo.duo = groomsman
                g_duo.save()
            messages.success(request, _('{} was updated!').format(form.cleaned_data["name"]), extra_tags='success')
            return redirect('ceremony:ceremony-groomsman-list')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        form = GroomsmanFrontForm(instance=groomsman)
    solo_groomsmen_ammount = Groomsman.objects.filter(duo__isnull=True).count()
    duo_groomsmen_ammount = int(Groomsman.objects.filter(duo__isnull=False).count() // 2)
    errors = False
    if Groomsman.objects.all().count() % 2 == 0 and solo_groomsmen_ammount % 2 != 0:
        errors = True
    context['form'] = form
    context['consistency_errors'] = errors
    context['solo_groomsmen_ammount'] = solo_groomsmen_ammount
    context['duo_groomsmen_ammount'] = duo_groomsmen_ammount
    context['edit'] = True
    return render(request, 'groomsmen/index.html', context=context)


def groomsman_delete(request, groomsman_id):
    Groomsman.objects.get(id=groomsman_id).delete()
    messages.success(request, _('Groomsman removed!'), extra_tags='success')
    return redirect('ceremony:ceremony-groomsman-list')


def category_create(request):
    response = dict()
    form = CategoryFrontForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, _('New category added!'), extra_tags='success')
        response['status'] = 'success'
    else:
        messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
        response['status'] = 'error'
    return JsonResponse(response)


def category_delete(request, category_id):
    response = dict()
    Category.objects.get(id=category_id).delete()
    response['status'] = 'success'
    return JsonResponse(response)


def provider_create(request):
    context = dict()
    if request.method == 'POST':
        form = ProviderFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('New provider added!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    form = ProviderFrontForm(data=request.GET) if request.GET else ProviderFrontForm()
    context['form'] = form
    return render(request, 'providers/index.html', context=context)


def provider_list(request):
    context = dict()
    providers = Provider.objects.all()
    context['providers'] = providers
    return render(request, 'providers/list.html', context=context)


def provider_delete(request, provider_id):
    Provider.objects.get(id=provider_id).delete()
    messages.success(request, _('Provider deleted!'), extra_tags='success')
    return redirect('ceremony:ceremony-provider-list')


def provider_update(request, provider_id):
    context = dict()
    provider = Provider.objects.get(id=provider_id)
    if request.method == 'POST':
        form = ProviderFrontForm(data=request.POST, files=request.FILES, instance=provider)
        form_is_valid = form.is_valid()
        if form_is_valid:
            form.save()
            messages.success(request, _('{} was updated!').format(form.cleaned_data["name"]), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        form = ProviderFrontForm(instance=provider)
    context['form'] = form
    context['edit'] = True
    return render(request, 'providers/index.html', context=context)


def set_provider_as_favorite(request, provider_id):
    response = dict()
    provider = Provider.objects.get(id=provider_id)
    provider.favorite = False if provider.favorite else True
    provider.save()
    response['status'] = 'success'
    return JsonResponse(response)


def music_create(request):
    context = dict()
    if request.method == 'POST':
        form = MusicFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('New music added!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    form = MusicFrontForm(data=request.GET) if request.GET else MusicFrontForm()
    context['form'] = form
    return render(request, 'musics/index.html', context=context)


def music_list(request):
    context = dict()
    musics = Music.objects.all()
    context['musics'] = musics
    context['song_occasions'] = Occasion.objects.all()
    return render(request, 'musics/list.html', context=context)


def music_delete(request, music_id):
    Music.objects.get(id=music_id).delete()
    messages.success(request, _('Song deleted!'), extra_tags='success')
    return redirect('ceremony:ceremony-music-list')


def music_update(request, music_id):
    context = dict()
    music = Music.objects.get(id=music_id)
    if request.method == 'POST':
        form = MusicFrontForm(data=request.POST, files=request.FILES, instance=music)
        form_is_valid = form.is_valid()
        if form_is_valid:
            form.save()
            messages.success(request, _('The song was updated!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        form = MusicFrontForm(instance=music)
    context['form'] = form
    context['edit'] = True
    return render(request, 'musics/index.html', context=context)


def ceremony_index(request):
    context = dict()
    if request.method == 'POST':
        try:
            ceremony = Ceremony.objects.get(id=1)
            form = CeremonyFrontForm(instance=ceremony, data=request.POST, files=request.FILES)
        except Ceremony.DoesNotExist:
            form = CeremonyFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Ceremony updated!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        try:
            ceremony = Ceremony.objects.get(id=1)
            form = CeremonyFrontForm(instance=ceremony)
        except Ceremony.DoesNotExist:
            form = CeremonyFrontForm()
    context['form'] = form
    return render(request, 'index.html', context=context)


def clothes_planner(request):
    context = dict()
    if request.method == 'POST':
        try:
            clothes_planner = ClothesPlanner.objects.get(id=1)
            form = ClothesPlannerFrontForm(instance=clothes_planner, data=request.POST, files=request.FILES)
        except ClothesPlanner.DoesNotExist:
            form = ClothesPlannerFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Clothes updated!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        try:
            clothes_planner = ClothesPlanner.objects.get(id=1)
            form = ClothesPlannerFrontForm(instance=clothes_planner)
        except ClothesPlanner.DoesNotExist:
            form = ClothesPlannerFrontForm()
    context['form'] = form
    return render(request, 'clothes_planner/index.html', context=context)


@require_POST
def occasion_create(request):
    response = dict()
    form = OccasionFrontForm(data)
    if form.is_valid():
        form.save()
        messages.success(request, _('New occasion added!'), extra_tags='success')
        response['status'] = 'success'
    else:
        messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
        response['status'] = 'error'
    return JsonResponse(response)


def occasion_delete(request, occasion_id):
    response = dict()
    Occasion.objects.get(id=occasion_id).delete()
    response['status'] = 'success'
    return JsonResponse(response)
