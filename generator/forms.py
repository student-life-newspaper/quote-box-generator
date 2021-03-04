from django import forms

class QuoteBoxForm(forms.Form):
    quote_text = forms.CharField(label='Quote text', max_length=500, widget=forms.Textarea)
    quote_citation = forms.CharField(label='Quote citation', max_length=200)
    background_color = forms.CharField(label='Background color (6 character hex value)', initial="e3070e", max_length=6)
    text_color = forms.CharField(label='Text color (6 character hex value)', initial="ffffff", max_length=6)
    width = forms.IntegerField(label="Width (px)", initial=1900)
    height = forms.IntegerField(label="Height (px)", initial=1200)