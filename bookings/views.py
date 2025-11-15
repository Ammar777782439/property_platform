from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from datetime import date

from .models import Booking, Offers
from .forms import BookingForm
from properties.models import Property


@login_required
def create_booking(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            offer_code = form.cleaned_data.get('offer_code')

            if start_date >= end_date:
                messages.error(request, 'نطاق التاريخ غير صالح')
                return redirect(reverse('property_detail', kwargs={'property_id': prop.pk}))

            nights = (end_date - start_date).days
            original_price = nights * prop.default_daily_price
            discount_amount = 0
            offer_obj = None
            if offer_code:
                offer_qs = Offers.objects.filter(code__iexact=offer_code, is_active=True)
                offer_qs = offer_qs.filter(property=prop) | offer_qs.filter(property__isnull=True)
                offer_obj = offer_qs.first()
                if offer_obj and offer_obj.is_valid:
                    discount_amount = offer_obj.calculate_discount(original_price)

            total_price = original_price - discount_amount
            if total_price < 0:
                total_price = 0

            # Check overlap
            overlap = Booking.objects.filter(
                property=prop,
                status__in=['pending_owner_approval', 'confirmed'],
                start_date__lt=end_date,
                end_date__gt=start_date,
            ).exists()
            if overlap:
                messages.error(request, 'التواريخ المختارة غير متاحة')
                return redirect(reverse('property_detail', kwargs={'property_id': prop.pk}))

            booking = Booking.objects.create(
                user=request.user,
                property=prop,
                offers=offer_obj,
                start_date=start_date,
                end_date=end_date,
                original_price=original_price,
                discount_amount=discount_amount,
                total_price=total_price,
            )
            return redirect('booking_confirm', booking_id=booking.booking_id)
    else:
        form = BookingForm()

    return render(request, 'properties/detail.html', {'property': prop, 'form': form})


@login_required
def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'bookings/confirm.html', {'booking': booking})
