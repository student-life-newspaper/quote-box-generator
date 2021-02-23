from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import QuoteBox

def index(request):
    message = "studlife is cool"
    try:
        quoteBox = QuoteBox.objects.get(pk=request.GET['id'])
    except QuoteBox.DoesNotExist:
        quoteBox = None
    context = {
        'message': message,
        'quoteBox' : quoteBox
    }
    return render(request, 'generator/index.html', context)