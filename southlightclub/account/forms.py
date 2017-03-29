from django import forms
from django.contrib.auth.models import User


class PasswordForm(forms.ModelForm):
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())
    password2 = forms.CharField(label='確認密碼', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', 'password2', )

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password!=password2:
            raise forms.ValidationError('密碼不相同')
        return password2

