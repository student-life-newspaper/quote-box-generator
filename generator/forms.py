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

TEXT_COLOR_CHOICES = [
    ('ffffff', 'White'),
    ('Custom','Custom')
]

CITATION_FONT_SIZE_CHOICES = [
    ('Same','Same as quote text'),
    ('Auto','Auto')
]

class QuoteBoxForm(forms.Form):
    quote_text = forms.CharField(label='Quote text', max_length=500, widget=forms.Textarea)
    quote_citation = forms.CharField(label='Quote citation', max_length=200)
    background_color = forms.ChoiceField(label="Background color", widget=forms.RadioSelect, initial=BACKGROUND_COLOR_CHOICES[0][0], choices=BACKGROUND_COLOR_CHOICES)
    background_color_custom = HexFormField(label='Custom background color (6 character hex value)', initial="", max_length=6, required=False, widget=forms.TextInput(attrs={'class' : 'custom_input'}))
    text_color = forms.ChoiceField(label='Text color', widget=forms.RadioSelect, initial=TEXT_COLOR_CHOICES[0][0],choices=TEXT_COLOR_CHOICES)
    text_color_custom = HexFormField(label='Custom text color (6 character hex value)', max_length=6, required=False, widget=forms.TextInput(attrs={'class' : 'custom_input'}))
    quote_font_size = forms.ChoiceField(label="Quote font size (pts)", widget=forms.RadioSelect, initial=QUOTE_FONT_SIZE_CHOICES[0][0], choices=QUOTE_FONT_SIZE_CHOICES)
    quote_font_size_custom = forms.IntegerField(label="Custom quote font size (pts)", initial=0, widget=forms.TextInput(attrs={'class' : 'custom_input'}), required=False)
    citation_font_size = forms.ChoiceField(label='Citation font size', widget=forms.RadioSelect, initial=CITATION_FONT_SIZE_CHOICES[0][0], choices=CITATION_FONT_SIZE_CHOICES)
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
        if quote_font_size == 'Custom':
            if not quote_font_size_custom:
                raise ValidationError(
                    'Please enter a custom quote font size'
                )
            elif quote_font_size_custom < 1 or quote_font_size_custom > 500:
                raise ValidationError(
                    'Font size must be greater than 0 and less than 500'
                )
        
        if cleaned_data.get('text_color') == 'Custom' and not cleaned_data.get('text_color_custom'):
            raise ValidationError(
                    'Please enter a custom text color'
            )
        
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')
        if width < 10 or width > 5000:
            raise ValidationError(
                'Width out of bounds'
            )
        if height < 10 or height > 5000:
            raise ValidationError(
                'Height out of bounds'
            )