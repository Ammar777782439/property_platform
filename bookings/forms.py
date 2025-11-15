from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='تاريخ البداية')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='تاريخ النهاية')
    offer_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label='كود الخصم (اختياري)')

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
