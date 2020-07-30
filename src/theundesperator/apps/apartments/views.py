from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST

from theundesperator.apps.apartments.forms import ApartmentFrontForm
from theundesperator.apps.apartments.models import Apartment


def apartment_list(request):
    context = dict()
    apartments = Apartment.objects.all()
    context['apartments'] = apartments
    return render(request, 'apartments/list.html', context=context)


def apartment_delete(request, apartment_id):
    Apartment.objects.get(id=apartment_id).delete()
    messages.success(request, _('Apartment deleted!'), extra_tags='success')
    return redirect('ceremony:ceremony-apartment-list')


def apartment_create(request):
    context = dict()
    if request.method == 'POST':
        form = ApartmentFrontForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('New apartment added!'), extra_tags='success')
            return redirect('apartment:apartment-list')
        else:
            messages.error(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    form = ApartmentFrontForm(data=request.GET) if request.GET else ApartmentFrontForm()
    context['form'] = form
    return render(request, 'apartments/index.html', context=context)


def apartment_details(request, apartment_id):
    context = dict()
    apartment = Apartment.objects.get(id=apartment_id)
    context['apartment'] = apartment
    return render(request, 'apartments/details.html', context=context)


def apartment_update(request, apartment_id):
    context = dict()
    apartment = Apartment.objects.get(id=apartment_id)
    if request.method == 'POST':
        form = ApartmentFrontForm(data=request.POST, instance=apartment)
        form_is_valid = form.is_valid()
        if form_is_valid:
            form.save()
            messages.success(request, _('{} was updated!').format(form.cleaned_data["name"]), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        form = ApartmentFrontForm(instance=apartment)
    context['form'] = form
    context['edit'] = True
    return render(request, 'apartments/index.html', context=context)


def set_apartment_as_favorite(request, apartment_id):
    response = dict()
    apartment = Apartment.objects.get(id=apartment_id)
    apartment.favorite = False if apartment.favorite else True
    apartment.save()
    response['status'] = 'success'
    return JsonResponse(response)


