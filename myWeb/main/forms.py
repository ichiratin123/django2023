from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm,PasswordResetForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Review,Checkout


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg rounded-3',
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg rounded-3',
        'placeholder': 'Password',
    }))

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg rounded-3',
        'placeholder': 'Email',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'Username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'Confirm Password',
        })
        
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Old Password',
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'New Password',
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Confirm New Password',
    }))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_(""),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'Email',
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'New password',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control form-control-lg rounded-3',
            'placeholder': 'Confirm new password',
        }),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=99)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    
class ReviewForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'class': 'form-control'})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']


class CheckoutForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
    ]

    shipping_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Checkout
        fields = ['shipping_address', 'payment_method']

