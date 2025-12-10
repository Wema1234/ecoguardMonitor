from django import forms
from .models import MediaAsset, EnvironmentalData

class MediaAssetForm(forms.ModelForm):
    class Meta:
        model = MediaAsset
        fields = ['title', 'description', 'category', 'media_file', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EnvironmentalDataForm(forms.ModelForm):
    class Meta:
        model = EnvironmentalData
        fields = ['data_type', 'location', 'value', 'unit', 'description', 'date_recorded', 'latitude', 'longitude']
        widgets = {
            'data_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Value'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows': 3}),
            'date_recorded': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}),
        }
