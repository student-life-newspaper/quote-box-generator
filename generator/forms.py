from django import forms

class QuoteBoxForm(forms.Form):
    quote_text = forms.CharField(label='Quote text', max_length=300)