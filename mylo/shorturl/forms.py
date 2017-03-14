from django import forms


from .validators import validate_url

class SubmitURLForm(forms.Form):
    url = forms.CharField(
        label="Submit URL", 
        validators=[validate_url],
        widget=forms.TextInput(
            attrs={
                'placeholder':"enter long url",
                'class': 'form-control',
            }
        ))

    