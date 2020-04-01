from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Listing
from .choices import price_choices, bedroom_choices, state_choices


def index(request):
    # - before column name gives acending order result
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'listings': page_obj
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing':  listing
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by(
        '-list_date').filter(is_published=True)

    # iexact and icontains are for case_unsensitive
    # icontains is for checkIfItContain
    # iexact is for checking Exact
    # lte is for less than

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)
    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(
                city__iexact=city)
    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            if 'State (All)' != state:
                queryset_list = queryset_list.filter(
                    state__iexact=state)
    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            if 'Max Price (All)' != price:
                queryset_list = queryset_list.filter(
                    price__lte=price)
    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            if 'Bedrooms (Any)' != bedrooms:
                queryset_list = queryset_list.filter(
                    bedrooms__lte=bedrooms)

    paginator = Paginator(queryset_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'listings': page_obj,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'request': request.GET
    }
    return render(request, 'listings/search.html', context)
