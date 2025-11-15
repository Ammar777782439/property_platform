from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from datetime import datetime

from .models import Property
from bookings.models import Booking


def _parse_date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except Exception:
        return None


def property_list(request):
    qs = Property.objects.select_related('owner').prefetch_related('images')

    q = request.GET.get('q')
    city = request.GET.get('city')
    guests = request.GET.get('guests')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    start = _parse_date(request.GET.get('start', ''))
    end = _parse_date(request.GET.get('end', ''))

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(address__icontains=q))
    if city:
        qs = qs.filter(city__icontains=city)
    if guests:
        try:
            qs = qs.filter(max_capacity__gte=int(guests))
        except ValueError:
            pass
    if price_min:
        try:
            qs = qs.filter(default_daily_price__gte=float(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            qs = qs.filter(default_daily_price__lte=float(price_max))
        except ValueError:
            pass
    if start and end and start < end:
        overlap_bookings = Booking.objects.filter(
            start_date__lt=end,
            end_date__gt=start,
            status__in=['pending_owner_approval', 'confirmed'],
        ).values_list('property_id', flat=True)
        qs = qs.exclude(pk__in=set(overlap_bookings))

    context = {
        'properties': qs,
    }
    return render(request, 'properties/list.html', context)


def property_detail(request, property_id):
    prop = get_object_or_404(
        Property.objects.select_related('owner').prefetch_related('images', 'reviews__user'),
        pk=property_id
    )
    context = {
        'property': prop,
    }
    return render(request, 'properties/detail.html', context)
