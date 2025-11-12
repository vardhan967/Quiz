from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import inlineformset_factory
from .models import Category, Question, Answer

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

    def __init__(self, *args, **kwargs):
        """Ensure widgets use the site's input class so styles apply."""
        super().__init__(*args, **kwargs)
        # Normalize widget classes for all visible fields
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            # replace form-control or other classes with our .input class
            widget.attrs['class'] = ('input' if not existing else existing.replace('form-control', 'input'))

class LoginForm(AuthenticationForm):
    """
    A simple login form.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder':'Password'}))


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            existing = f.widget.attrs.get('class', '')
            f.widget.attrs['class'] = existing.replace('form-control', 'input') if existing else 'input'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'question_text', 'marks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            existing = f.widget.attrs.get('class', '')
            f.widget.attrs['class'] = existing.replace('form-control', 'input') if existing else 'input'


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            existing = f.widget.attrs.get('class', '')
            f.widget.attrs['class'] = existing.replace('form-control', 'input') if existing else 'input'


# Inline formset: Answers tied to a Question
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=3, can_delete=True)
