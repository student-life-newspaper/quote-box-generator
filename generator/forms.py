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

QUOTE_FONT_SIZE_CHOICES = [
    ('Auto','Auto'),
    ('Custom','Custom'),
]

class QuoteBoxForm(forms.Form):
    quote_text = forms.CharField(label='Quote text', max_length=500, widget=forms.Textarea)
    quote_citation = forms.CharField(label='Quote citation', max_length=200)
    background_color = forms.ChoiceField(label="Background color", widget=forms.RadioSelect, initial=BACKGROUND_COLOR_CHOICES[0][0], choices=BACKGROUND_COLOR_CHOICES)
    background_color_custom = HexFormField(label='Custom background color (6 character hex value)', initial="", max_length=6, required=False)
    text_color = HexFormField(label='Text color (6 character hex value)', initial="ffffff", max_length=6)
    quote_font_size = forms.ChoiceField(label="Quote font size (pts)", widget=forms.RadioSelect, initial=QUOTE_FONT_SIZE_CHOICES[0][0], choices=QUOTE_FONT_SIZE_CHOICES)
    quote_font_size_custom = forms.IntegerField(label="Custom quote font size (px)", initial=0, required=False)
    width = forms.IntegerField(label="Width (px)", initial=950)
    height = forms.IntegerField(label="Height (px)", initial=600)

    def clean(self):
        cleaned_data = super().clean()
        background_color = cleaned_data.get("background_color")
        background_color_custom = cleaned_data.get("background_color_custom")

        if background_color == "Custom" and not background_color_custom:
            raise ValidationError(
                "Please enter a valid background color"
            )

        quote_font_size = cleaned_data.get("quote_font_size")
        quote_font_size_custom = cleaned_data.get("quote_font_size_custom")
        if quote_font_size == 'Custom' and not quote_font_size_custom:
            raise ValidationError(
                'Please enter a custom quote font size'
            )
