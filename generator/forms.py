import re

from django import forms

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

class QuoteBoxForm(forms.Form):
    quote_text = forms.CharField(label='Quote text', max_length=500, widget=forms.Textarea)
    quote_citation = forms.CharField(label='Quote citation', max_length=200)
    background_color = HexFormField(label='Background color (6 character hex value)', initial="e3070e", max_length=6)
    text_color = HexFormField(label='Text color (6 character hex value)', initial="ffffff", max_length=6)
    width = forms.IntegerField(label="Width (px)", initial=1116)
    height = forms.IntegerField(label="Height (px)", initial=706)