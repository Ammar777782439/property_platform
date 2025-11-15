from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='الاسم الأول', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, label='الاسم الأخير', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='البريد الإلكتروني', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, max_length=20, label='رقم الهاتف', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'اسم المستخدم'
        for name in ['username', 'password1', 'password2']:
            if name in self.fields:
                self.fields[name].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'كلمة المرور'
        self.fields['password2'].label = 'تأكيد كلمة المرور'
