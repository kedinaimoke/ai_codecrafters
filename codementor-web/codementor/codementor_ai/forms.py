from django import forms

class BaseForm(forms.Form):
    input_field = forms.CharField(label='Input', widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Enter your code or input here...'}))
