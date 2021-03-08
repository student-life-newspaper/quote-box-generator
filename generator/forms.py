import re

from django import forms
from django.core.exceptions import ValidationError

# adapted from https://gist.github.com/ostcar/9589152
class HexFormField(forms.CharField):
    default_error_messages = {
        'invalid': 'Enter a valid hexfigure: e.g. "ff0022"',
    }

    def clean(self, value):
        if (not (value == '' and not self.required) and
                not re.match('^[A-Fa-f0-9]{6}$', value)):
            raise forms.ValidationError(self.error_messages['invalid'])
        return value

BACKGROUND_COLOR_CHOICES = [
    ('b1170f','Red'),
    ('696969','Grey'),
    ('007d2c','Green'),
    ('0e1e5c','Blue'),
    ('Custom','Custom'),
]

class QuoteBoxForm(forms.Form):
    quote_text = forms.CharField(label='Quote text', max_length=500, widget=forms.Textarea)
    quote_citation = forms.CharField(label='Quote citation', max_length=200)
    background_color = forms.ChoiceField(label="Background color", widget=forms.RadioSelect, choices=BACKGROUND_COLOR_CHOICES)
    background_color_custom = HexFormField(label='Custom background color (6 character hex value)', initial="", max_length=6, required=False)
    text_color = HexFormField(label='Text color (6 character hex value)', initial="ffffff", max_length=6)
    width = forms.IntegerField(label="Width (px)", initial=1116)
    height = forms.IntegerField(label="Height (px)", initial=706)

    def clean(self):
        cleaned_data = super().clean()
        background_color = cleaned_data.get("background_color")
        background_color_custom = cleaned_data.get("background_color_custom")

        if background_color == "Custom" and not background_color_custom:
            raise ValidationError(
                "Please enter a valid background color"
            )
            