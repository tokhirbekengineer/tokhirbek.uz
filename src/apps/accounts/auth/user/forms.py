from django import forms
from django.contrib.auth.forms import AuthenticationForm
from apps.accounts.models.custom_user import CustomUser

class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Parol'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username_email', 'reset_password_email', 'password']
        widgets = {
            'username_email': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Username yoki Email'
            }),
            'reset_password_email': forms.EmailInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Email (parolni tiklash uchun)'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_classes = 'w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500'

        self.fields['username'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Email yoki Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': common_classes,
            'placeholder': 'Parol'
        })
