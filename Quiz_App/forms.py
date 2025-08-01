from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(UserCreationForm):
    """
    A form for creating new users. Includes a password confirmation field.
    """
    email = forms.EmailField(required=True, help_text='Required. Inform a valid email address.')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_password2(self):
        """
        Verify that the two password fields match.
        This method is now more robust to prevent KeyErrors.
        """
        cd = self.cleaned_data
        # Safely get the password fields from cleaned_data.
        # If the first password field failed validation, .get() will return None
        # instead of raising a KeyError.
        password = cd.get("password")
        password2 = cd.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match.")
        
        return password2

class LoginForm(AuthenticationForm):
    """
    A simple login form.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))
