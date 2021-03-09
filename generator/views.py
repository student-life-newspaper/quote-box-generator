from PIL import Image, ImageDraw, ImageFont, ImageColor
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.http import urlencode
from .forms import QuoteBoxForm

# text_wrap adapted from https://github.com/Eyongkevin/How-to-Wrap-Text-on-Image-using-Python/
def text_wrap(text, font, max_width):
    lines = []
    
    # If the text width is smaller than the image width, then no need to split
    # just add it to the line list and return
    if font.getsize(text)[0]  <= max_width:
        lines.append(text)
    else:
        #split the line by spaces to get words
        words = text.split(' ')
        i = 0
        # append every word to a line while its width is shorter than the image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i]+ " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines

def generate_quote_box(request):
    if request.method == "GET":
        form = QuoteBoxForm(request.GET)
        if form.is_valid():
            qb = form.cleaned_data

            if qb['background_color'] == 'Custom':
                form_background_color = qb['background_color_custom']
            else:
                form_background_color = qb['background_color']
            background_color = ImageColor.getrgb('#' + form_background_color)
            text_color = ImageColor.getrgb('#' + qb['text_color'])

            imageWidth = qb['width']
            imageHeight = qb['height']

            im = Image.new("RGB", (imageWidth,imageHeight), color=background_color)
            draw = ImageDraw.Draw(im)

            # define bars
            barMargin = (int)(imageWidth / 27)
            barWeight = (int)(imageWidth / 43)
            barHorizontalLength = imageWidth * 0.4
            barVerticalLength = imageHeight * 0.35
            barColor = text_color

            # draw upper bars
            draw.rectangle([barMargin, barMargin, barHorizontalLength, barMargin + barWeight], fill=barColor)
            draw.rectangle([barMargin, barMargin, barMargin + barWeight, barVerticalLength], fill=barColor)
            # draw lower bars
            draw.rectangle([imageWidth - barMargin - barHorizontalLength, imageHeight - barMargin - barWeight, imageWidth - barMargin, imageHeight - barMargin], fill=barColor)
            draw.rectangle([imageWidth - barMargin, imageHeight - barMargin, imageWidth - barMargin - barWeight, imageHeight - barWeight - barVerticalLength], fill=barColor)

            # import font
            quote_font = ImageFont.truetype("/app/fonts/Georgia.ttf", size=57)
            text = qb['quote_text']

            # get lines to wrap text
            quote_lines = text_wrap(text, quote_font, (imageWidth - 6 * barMargin))

            line_height = quote_font.getsize('hg')[1]

            # quote positioning
            quote_x = 2 * barMargin + barWeight
            quote_y = 1.75 * barMargin + barWeight

            # print quote lines
            for line in quote_lines:
                draw.text((quote_x,quote_y), line, fill=text_color, font=quote_font)
                quote_y = quote_y + line_height

            # set citation
            quote_citation = "— " + qb['quote_citation']

            # calculate citation width
            citation_font = ImageFont.truetype("/app/fonts/Georgia.ttf", size=50)
            target_size = imageWidth * 0.6
            current_citation_width = citation_font.getsize(quote_citation)[0]
            new_citation_font_size = (target_size / current_citation_width) * 50
            citation_font = ImageFont.truetype("/app/fonts/Georgia.ttf", size=int(new_citation_font_size))
            quote_citation_size = citation_font.getsize(quote_citation)
            quote_citation_position = ((imageWidth - (3 * barMargin) - quote_citation_size[0]), 
                                        (imageHeight - (2.5 * barMargin) - quote_citation_size[1]))

            draw.text((quote_citation_position[0],quote_citation_position[1]), quote_citation, font=citation_font)
        else:
            im = Image.new("RGB", (600,200), color=(227, 7, 14))
            draw = ImageDraw.Draw(im)
            quote_font = ImageFont.truetype("/app/fonts/Georgia.ttf", size=40)
            draw.text((50,50), 'An error has occured', fill=(255,255,255), font=quote_font)

    response = HttpResponse(content_type="image/png")
    im.save(response, "PNG")
    return response

def index(request):
    if request.method == "POST":
        form = QuoteBoxForm(request.POST)
        if form.is_valid():
            qb_url = "generate_quote_box?"
            qb_url = qb_url + urlencode(form.cleaned_data)
        else:
            qb_url = None
    else:
        qb_url = None
        form = QuoteBoxForm()

    context = {
        'form' : form,
        'qb_url': qb_url
    }

    return render(request, 'generator/index.html', context)