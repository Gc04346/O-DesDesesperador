from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST

from theundesperator.apps.apartments.forms import ApartmentFrontForm, RoomFrontForm, ExpenseFrontForm, ItemFrontForm
from theundesperator.apps.apartments.models import Apartment, Room, Expense, Item


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
        form = ApartmentFrontForm(data=request.POST, files=request.FILES)
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
        form = ApartmentFrontForm(data=request.POST, files=request.FILES, instance=apartment)
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


def room_list(request):
    context = dict()
    rooms = Room.objects.all()
    context['rooms'] = rooms
    expenses = Expense.objects.all()
    context['expenses'] = expenses
    return render(request, 'rooms/index.html', context=context)


@require_POST
def room_create(request):
    form = RoomFrontForm(data=request.POST, files=request.FILES)
    response = dict()
    form_is_valid = form.is_valid()
    if form_is_valid:
        form.save()
        messages.success(request, _('Room added!'), extra_tags='success')
        response['status'] = 'success'
    else:
        messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
        response['status'] = 'error'
        response['data'] = form_is_valid
    return JsonResponse(response)


def room_delete(request, room_id):
    response = dict()
    Room.objects.get(id=room_id).delete()
    return JsonResponse(response)


@require_POST
def expense_create(request):
    form = ExpenseFrontForm(data=request.POST, files=request.FILES)
    response = dict()
    form_is_valid = form.is_valid()
    if form_is_valid:
        form.save()
        messages.success(request, _('Expense added!'), extra_tags='success')
        response['status'] = 'success'
    else:
        messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
        response['status'] = 'error'
        response['data'] = form_is_valid
    return JsonResponse(response)


def expense_delete(request, expense_id):
    response = dict()
    Expense.objects.get(id=expense_id).delete()
    return JsonResponse(response)


def room_detail(request, room_id):
    context = dict()
    room = Room.objects.get(id=room_id)
    items = Item.objects.filter(room=room)
    context['items'] = items
    context['room'] = room
    return render(request, 'items/index.html', context=context)


def item_delete(request, item_id):
    item = Item.objects.get(id=item_id)
    room = item.room
    item.delete()
    return JsonResponse({'status': 'success'})
    return redirect('apartment:room-detail', room_id=room.id)


def item_list(request):
    context = dict()
    context['items'] = Item.objects.all()
    context['rooms'] = Room.objects.all()
    return render(request, 'items/list.html', context=context)


@require_POST
def item_create(request):
    response = dict()
    form = ItemFrontForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, _('Item added!'), extra_tags='success')
        response['status'] = 'success'
    else:
        messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
        response['status'] = 'error'
    return JsonResponse(response)


def mark_unmark_item(request, item_id):
    response = dict()
    item = Item.objects.get(id=item_id)
    item.done = False if item.done else True
    item.save()
    response['status'] = 'success'
    return JsonResponse(response)
