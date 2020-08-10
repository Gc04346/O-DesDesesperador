from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST

from theundesperator.apps.honeymoon.forms import HoneymoonOrganizerFrontForm, BudgetFrontForm
from theundesperator.apps.honeymoon.models import HoneymoonOrganizer, Budget


def honeymoon_organizer_index(request):
    context = dict()
    if request.method == 'POST':
        try:
            honeymoon_organizer = HoneymoonOrganizer.objects.get(id=1)
            form = HoneymoonOrganizerFrontForm(instance=honeymoon_organizer, data=request.POST, files=request.FILES)
        except HoneymoonOrganizer.DoesNotExist:
            form = HoneymoonOrganizerFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Honeymoon updated!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        try:
            honeymoon_organizer = HoneymoonOrganizer.objects.get(id=1)
            form = HoneymoonOrganizerFrontForm(instance=honeymoon_organizer)
        except HoneymoonOrganizer.DoesNotExist:
            form = HoneymoonOrganizerFrontForm()
    context['form'] = form
    return render(request, 'honeymoon/index.html', context=context)


def budget_create(request):
    context = dict()
    if request.method == 'POST':
        form = BudgetFrontForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('New budget added!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    form = BudgetFrontForm(data=request.GET) if request.GET else BudgetFrontForm()
    context['form'] = form
    return render(request, 'budgets/index.html', context=context)


def budget_list(request):
    context = dict()
    budgets = Budget.objects.all()
    context['budgets'] = budgets
    return render(request, 'budgets/list.html', context=context)


def budget_delete(request, budget_id):
    Budget.objects.get(id=budget_id).delete()
    messages.success(request, _('Budget deleted!'), extra_tags='success')
    return redirect('honeymoon:budget-list')


def budget_update(request, budget_id):
    context = dict()
    budget = Budget.objects.get(id=budget_id)
    if request.method == 'POST':
        form = BudgetFrontForm(data=request.POST, files=request.FILES, instance=budget)
        form_is_valid = form.is_valid()
        if form_is_valid:
            form.save()
            messages.success(request, _('Budget updated!'), extra_tags='success')
        else:
            messages.warning(request, _('Fix the validation errors below before saving!'), extra_tags='error')
    else:
        form = BudgetFrontForm(instance=budget)
    context['form'] = form
    context['edit'] = True
    return render(request, 'budgets/index.html', context=context)

