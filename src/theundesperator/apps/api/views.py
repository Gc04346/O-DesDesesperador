from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer, ApartmentSerializer, ExpenseSerializer, ItemSerializer, CategorySerializer, \
    CeremonySerializer, ClothesPlannerSerializer, GroomsmanSerializer, GuestSerializer, MusicSerializer, \
    OccasionSerializer, ProviderSerializer, BudgetSerializer, HoneymoonOrganizerSerializer, DecorationSerializer, \
    PanTeaGuestSerializer, PanTeaOrganizerSerializer
from theundesperator.apps.apartments.models import Room, Apartment, Expense, Item
from theundesperator.apps.ceremony.models import Provider, Occasion, Guest, Groomsman, ClothesPlanner, Music, Ceremony, \
    Category
from theundesperator.apps.honeymoon.models import Budget, HoneymoonOrganizer
from theundesperator.apps.pantea.models import Decoration, PanTeaGuest, PanTeaOrganizer


@api_view(['GET'])
def overview(request):
    api_urls = {
        'List': 'app-name/model-name/list',
        'Detail': 'app-name/model-name/detail/<int:pk>',
        'Create': 'app-name/model-name/create',
        'Update': 'app-name/model-name/update/<int:pk>',
        'Delete': 'app-name/model-name/delete/<int:pk>',
    }
    return Response(api_urls)


# ================================== #
#          APP APARTMENTS            #
# ================================== #


# ------- Room ------- #
@api_view(['GET'])
def room_list(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def room_detail(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def room_create(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def room_update(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(instance=room, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def room_delete(request, pk):
    room = Room.objects.get(id=pk)
    room.delete()
    return Response('Room deleted!')


# ------- Apartment ------- #
@api_view(['GET'])
def apartment_list(request):
    apartments = Apartment.objects.all()
    serializer = ApartmentSerializer(apartments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def apartment_detail(request, pk):
    apartment = Apartment.objects.get(id=pk)
    serializer = ApartmentSerializer(apartment, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def apartment_create(request):
    serializer = ApartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def apartment_update(request, pk):
    apartment = Apartment.objects.get(id=pk)
    serializer = ApartmentSerializer(instance=apartment, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def apartment_delete(request, pk):
    apartment = Apartment.objects.get(id=pk)
    apartment.delete()
    return Response('Apartment deleted!')


# ------- Expense ------- #
@api_view(['GET'])
def expense_list(request):
    expenses = Expense.objects.all()
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def expense_detail(request, pk):
    expense = Expense.objects.get(id=pk)
    serializer = ExpenseSerializer(expense, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def expense_create(request):
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def expense_update(request, pk):
    expense = Expense.objects.get(id=pk)
    serializer = ExpenseSerializer(instance=expense, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def expense_delete(request, pk):
    expense = Expense.objects.get(id=pk)
    expense.delete()
    return Response('Expense deleted!')


# ------- Item ------- #
@api_view(['GET'])
def item_list(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def item_detail(request, pk):
    item = Item.objects.get(id=pk)
    serializer = ItemSerializer(item, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def item_create(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def item_update(request, pk):
    item = Item.objects.get(id=pk)
    serializer = ItemSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def item_delete(request, pk):
    item = Item.objects.get(id=pk)
    item.delete()
    return Response('Item deleted!')


# ================================== #
#            APP CEREMONY            #
# ================================== #


# ------- Category ------- #
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, pk):
    category = Category.objects.get(id=pk)
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def category_update(request, pk):
    category = Category.objects.get(id=pk)
    serializer = CategorySerializer(instance=category, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def category_delete(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return Response('Category deleted!')


# ------- Ceremony ------- #
@api_view(['GET'])
def ceremony_list(request):
    ceremonies = Ceremony.objects.all()
    serializer = CeremonySerializer(ceremonies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ceremony_detail(request, pk):
    ceremony = Ceremony.objects.get(id=pk)
    serializer = CeremonySerializer(ceremony, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def ceremony_create(request):
    serializer = CeremonySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def ceremony_update(request, pk):
    ceremony = Ceremony.objects.get(id=pk)
    serializer = CeremonySerializer(instance=ceremony, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def ceremony_delete(request, pk):
    ceremony = Ceremony.objects.get(id=pk)
    ceremony.delete()
    return Response('Ceremony deleted!')


# ------- Music ------- #
@api_view(['GET'])
def music_list(request):
    musics = Music.objects.all()
    serializer = MusicSerializer(musics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def music_detail(request, pk):
    music = Music.objects.get(id=pk)
    serializer = MusicSerializer(music, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def music_create(request):
    serializer = MusicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def music_update(request, pk):
    music = Music.objects.get(id=pk)
    serializer = MusicSerializer(instance=music, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def music_delete(request, pk):
    music = Music.objects.get(id=pk)
    music.delete()
    return Response('Music deleted!')


# ------- ClothesPlanner ------- #
@api_view(['GET'])
def clothes_planner_list(request):
    clothes_planners = ClothesPlanner.objects.all()
    serializer = ClothesPlannerSerializer(clothes_planners, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def clothes_planner_detail(request, pk):
    clothes_planner = ClothesPlanner.objects.get(id=pk)
    serializer = ClothesPlannerSerializer(clothes_planner, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def clothes_planner_create(request):
    serializer = ClothesPlannerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def clothes_planner_update(request, pk):
    clothes_planner = ClothesPlanner.objects.get(id=pk)
    serializer = ClothesPlannerSerializer(instance=clothes_planner, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def clothes_planner_delete(request, pk):
    clothes_planner = ClothesPlanner.objects.get(id=pk)
    clothes_planner.delete()
    return Response('ClothesPlanner deleted!')


# ------- Groomsman ------- #
@api_view(['GET'])
def groomsman_list(request):
    groomsmen = Groomsman.objects.all()
    serializer = GroomsmanSerializer(groomsmen, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def groomsman_detail(request, pk):
    groomsman = Groomsman.objects.get(id=pk)
    serializer = GroomsmanSerializer(groomsman, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def groomsman_create(request):
    serializer = GroomsmanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def groomsman_update(request, pk):
    groomsman = Groomsman.objects.get(id=pk)
    serializer = GroomsmanSerializer(instance=groomsman, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def groomsman_delete(request, pk):
    groomsman = Groomsman.objects.get(id=pk)
    groomsman.delete()
    return Response('Groomsman deleted!')


# ------- Guest ------- #
@api_view(['GET'])
def guest_list(request):
    guests = Guest.objects.all()
    serializer = GuestSerializer(guests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def guest_detail(request, pk):
    guest = Guest.objects.get(id=pk)
    serializer = GuestSerializer(guest, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def guest_create(request):
    serializer = GuestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def guest_update(request, pk):
    guest = Guest.objects.get(id=pk)
    serializer = GuestSerializer(instance=guest, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def guest_delete(request, pk):
    guest = Guest.objects.get(id=pk)
    guest.delete()
    return Response('Guest deleted!')


# ------- Occasion ------- #
@api_view(['GET'])
def occasion_list(request):
    occasions = Occasion.objects.all()
    serializer = OccasionSerializer(occasions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def occasion_detail(request, pk):
    occasion = Occasion.objects.get(id=pk)
    serializer = OccasionSerializer(occasion, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def occasion_create(request):
    serializer = OccasionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def occasion_update(request, pk):
    occasion = Occasion.objects.get(id=pk)
    serializer = OccasionSerializer(instance=occasion, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def occasion_delete(request, pk):
    occasion = Occasion.objects.get(id=pk)
    occasion.delete()
    return Response('Occasion deleted!')


# ------- Provider ------- #
@api_view(['GET'])
def provider_list(request):
    providers = Provider.objects.all()
    serializer = ProviderSerializer(providers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def provider_detail(request, pk):
    provider = Provider.objects.get(id=pk)
    serializer = ProviderSerializer(provider, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def provider_create(request):
    serializer = ProviderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def provider_update(request, pk):
    provider = Provider.objects.get(id=pk)
    serializer = ProviderSerializer(instance=provider, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def provider_delete(request, pk):
    provider = Provider.objects.get(id=pk)
    provider.delete()
    return Response('Provider deleted!')


# ================================== #
#           APP HONEYMOON            #
# ================================== #


# ------- Budget ------- #
@api_view(['GET'])
def budget_list(request):
    budgets = Budget.objects.all()
    serializer = BudgetSerializer(budgets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def budget_detail(request, pk):
    budget = Budget.objects.get(id=pk)
    serializer = BudgetSerializer(budget, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def budget_create(request):
    serializer = BudgetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def budget_update(request, pk):
    budget = Budget.objects.get(id=pk)
    serializer = BudgetSerializer(instance=budget, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def budget_delete(request, pk):
    budget = Budget.objects.get(id=pk)
    budget.delete()
    return Response('Budget deleted!')


# ------- HoneymoonOrganizer ------- #
@api_view(['GET'])
def honeymoon_organizer_list(request):
    honeymoon_organizers = HoneymoonOrganizer.objects.all()
    serializer = HoneymoonOrganizerSerializer(honeymoon_organizers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def honeymoon_organizer_detail(request, pk):
    honeymoon_organizer = HoneymoonOrganizer.objects.get(id=pk)
    serializer = HoneymoonOrganizerSerializer(honeymoon_organizer, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def honeymoon_organizer_create(request):
    serializer = HoneymoonOrganizerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def honeymoon_organizer_update(request, pk):
    honeymoon_organizer = HoneymoonOrganizer.objects.get(id=pk)
    serializer = HoneymoonOrganizerSerializer(instance=honeymoon_organizer, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def honeymoon_organizer_delete(request, pk):
    honeymoon_organizer = HoneymoonOrganizer.objects.get(id=pk)
    honeymoon_organizer.delete()
    return Response('HoneymoonOrganizer deleted!')


# ================================== #
#             APP PANTEA             #
# ================================== #


# ------- Decoration ------- #
@api_view(['GET'])
def decoration_list(request):
    decorations = Decoration.objects.all()
    serializer = DecorationSerializer(decorations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def decoration_detail(request, pk):
    decoration = Decoration.objects.get(id=pk)
    serializer = DecorationSerializer(decoration, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def decoration_create(request):
    serializer = DecorationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def decoration_update(request, pk):
    decoration = Decoration.objects.get(id=pk)
    serializer = DecorationSerializer(instance=decoration, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def decoration_delete(request, pk):
    decoration = Decoration.objects.get(id=pk)
    decoration.delete()
    return Response('Decoration deleted!')


# ------- PanTeaGuest ------- #
@api_view(['GET'])
def pan_tea_guest_list(request):
    pan_tea_guests = PanTeaGuest.objects.all()
    serializer = PanTeaGuestSerializer(pan_tea_guests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def pan_tea_guest_detail(request, pk):
    pan_tea_guest = PanTeaGuest.objects.get(id=pk)
    serializer = PanTeaGuestSerializer(pan_tea_guest, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def pan_tea_guest_create(request):
    serializer = PanTeaGuestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def pan_tea_guest_update(request, pk):
    pan_tea_guest = PanTeaGuest.objects.get(id=pk)
    serializer = PanTeaGuestSerializer(instance=pan_tea_guest, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def pan_tea_guest_delete(request, pk):
    pan_tea_guest = PanTeaGuest.objects.get(id=pk)
    pan_tea_guest.delete()
    return Response('PanTeaGuest deleted!')


# ------- PanTeaOrganizer ------- #
@api_view(['GET'])
def pan_tea_organizer_list(request):
    pan_tea_organizers = PanTeaOrganizer.objects.all()
    serializer = PanTeaOrganizerSerializer(pan_tea_organizers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def pan_tea_organizer_detail(request, pk):
    pan_tea_organizer = PanTeaOrganizer.objects.get(id=pk)
    serializer = PanTeaOrganizerSerializer(pan_tea_organizer, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def pan_tea_organizer_create(request):
    serializer = PanTeaOrganizerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def pan_tea_organizer_update(request, pk):
    pan_tea_organizer = PanTeaOrganizer.objects.get(id=pk)
    serializer = PanTeaOrganizerSerializer(instance=pan_tea_organizer, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def pan_tea_organizer_delete(request, pk):
    pan_tea_organizer = PanTeaOrganizer.objects.get(id=pk)
    pan_tea_organizer.delete()
    return Response('PanTeaOrganizer deleted!')
