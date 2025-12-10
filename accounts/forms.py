from django import forms

# Import the local User model before importing django.contrib.auth.forms so
# get_user_model() won't run before the model is registered.
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
#Registration form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control',
                                                                        'placeholder':'Email'}))
    
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
                                                                    
    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'profile_picture', 'bio', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Username'
            })
        }
    # passwords
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

# Login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={ 
         'class':'form-control',
         'placeholder':'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
       'class':'form-control',
       'placeholder':'Password'
    }))
# profile form : update on account profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_picture', 'bio')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class' : 'form-control', 'rows' : 3}),
        }
    