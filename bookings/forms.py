from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='تاريخ البداية')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='تاريخ النهاية')
    guests = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='عدد الضيوف')

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'guests']
