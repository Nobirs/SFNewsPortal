from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


from allauth.account.forms import SignupForm



class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        commoners = Group.objects.get(name='commoners')
        user.groups.add(commoners)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]