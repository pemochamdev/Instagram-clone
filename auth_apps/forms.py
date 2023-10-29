################ Author: https://github.com/pemochamdev #####################

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from auth_apps.models import Profile

def forbbiden_user(value):
    list_word =[
        'js', 'user', 'python', 'str', 'java',
        'log', 'login', 'logout', 'auth','admin',
        'delete', 'remove', 'add', 'filter', 'this',
        'super'
    ]
    if value.lower() in list_word:
        raise ValidationError('Reserve word')

def invalid_user(value):
    list_symbol = [
        '!','@','#','$','%','^','&','*','()','~','`',
        'or', 'in', 'and', ''
    ]
    if value in list_symbol:
        raise ValidationError('Invalid User, Do not use this carater')

def unique_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('This email already exist, please change')



class SignUpForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder':'Your email here'
        }),
        required=False
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder':'Your Username here'
        }),
        required=True
    )
    password = forms.CharField(
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Your password here'
        }),
        required=True
    )
    confirm_password = forms.CharField(
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Confirm your password here'
        }),
        required=True
    )
    class Meta:
        model = User
        fields = ("username", "email", "password")
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(forbbiden_user)
        self.fields['username'].validators.append(forbbiden_user)
        self.fields['email'].validators.append(unique_email)
    
    def clean(self, *args, **kwargs):
        super(SignUpForm, self).clean(*args, **kwargs)
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Password do not match. Please try again'])
        return self.cleaned_data




class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(
        widget=forms.HiddenInput()
    )
    old_password = forms.CharField(
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Your old_password here'
        }),
        required=True
    )
    new_password = forms.CharField(
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Your new_password here'
        }),
        required=True
    )
    confirm_password = forms.CharField(
        max_length=100,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Confirm your new password here'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')
    
    def clean(self, *args, **kwargs):
        super(ChangePasswordForm, self).clean(*args, **kwargs)
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] =self.error_class(['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] =self.error_class(['Passwords do not match.'])
        return self.cleaned_data


class ProfileEditeForm(forms.ModelForm):

    picture = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(), required=False)
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(), required=False)
    location = forms.CharField(max_length=200, widget=forms.TextInput(), required=False)
    
    description = forms.CharField( widget=forms.TextInput(), max_length=500, required=False)
    
    

    class Meta:
        model = Profile
        fields = ('picture', 'first_name', 'last_name', 'location',  'description', )

       

