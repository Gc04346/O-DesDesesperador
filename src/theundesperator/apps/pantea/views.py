from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST

from theundesperator.apps.pantea.forms import PanTeaOrganizerFrontForm, PanTeaGuestFrontForm, DecorationFrontForm
from theundesperator.apps.pantea.models import PanTeaOrganizer, PanTeaGuest, Decoration


def pan_tea_index(request):
    context = dict()
    if request.method == 'POST':
        try:
            pan_tea = PanTeaOrganizer.objects.get(id=1)
            form = PanTeaOrganizerFrontForm(instance=pan_tea, data=request.POST, files=request.FILES)
        except PanTeaOrganizer.DoesNotExist:
            form = PanTeaOrganizerFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('PanTeaOrganizer updated!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        try:
            pan_tea = PanTeaOrganizer.objects.get(id=1)
            form = PanTeaOrganizerFrontForm(instance=pan_tea)
        except PanTeaOrganizer.DoesNotExist:
            form = PanTeaOrganizerFrontForm()
    context['form'] = form
    return render(request, 'pantea/index.html', context=context)


def pan_tea_guest_create(request):
    context = dict()
    if request.method == 'POST':
        form = PanTeaGuestFrontForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('{} was added to the pantea guest list!').format(form.cleaned_data["name"]),
                             extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    form = PanTeaGuestFrontForm()
    pan_tea_guests_ammount = PanTeaGuest.objects.all().count()
    context['form'] = form
    context['guests_ammount'] = pan_tea_guests_ammount
    return render(request, 'pantea/guests/index.html', context=context)


def pan_tea_guest_list(request):
    context = dict()
    pan_tea_guests = PanTeaGuest.objects.all()
    context['guests'] = pan_tea_guests
    context['guests_ammount'] = pan_tea_guests.count()
    return render(request, 'pantea/guests/list.html', context=context)


@require_POST
def pan_tea_guest_update(request, pan_tea_guest_id):
    pan_tea_guest = PanTeaGuest.objects.get(id=pan_tea_guest_id)
    form = PanTeaGuestFrontForm(data=request.POST, files=request.FILES, instance=pan_tea_guest)
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


def pan_tea_guest_delete(request, pan_tea_guest_id):
    PanTeaGuest.objects.get(id=pan_tea_guest_id).delete()
    return redirect('pantea:pan_tea_guest-list')


def decoration_create(request):
    context = dict()
    if request.method == 'POST':
        form = DecorationFrontForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('New decoration added!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    form = DecorationFrontForm(data=request.GET) if request.GET else DecorationFrontForm()
    context['form'] = form
    return render(request, 'pantea/decorations/index.html', context=context)


@require_POST
def notemplate_decoration_create(request):
    response = dict()
    form = DecorationFrontForm(request.POST, files=request.FILES)
    form_is_valid = form.is_valid()
    if form_is_valid:
        form.save()
        messages.success(request, _('New decoration added!'), extra_tags='success')
        response['status'] = 'success'
    else:
        messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
        response['status'] = 'error'
        response['data'] = form_is_valid
    return JsonResponse(response)


def decoration_list(request):
    context = dict()
    decorations = Decoration.objects.all()
    context['decorations'] = decorations
    return render(request, 'pantea/decorations/list.html', context=context)


def decoration_delete(request, decoration_id):
    Decoration.objects.get(id=decoration_id).delete()
    messages.success(request, _('Decoration deleted!'), extra_tags='success')
    return redirect('ceremony:ceremony-decoration-list')
