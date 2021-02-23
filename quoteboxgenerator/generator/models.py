from django.db import models

# Create your models here.

class QuoteBox(models.Model):
    quote_text = models.CharField(max_length=400)
    quote_citation = models.CharField(max_length=200)
    background_color = models.CharField(max_length=6)
    text_color = models.CharField(max_length=6)

    def __str__(self):
        return "A quote by " + self.quote_citation