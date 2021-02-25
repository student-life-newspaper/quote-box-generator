import os, sys
from PIL import Image, ImageDraw, ImageFont

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

imageWidth = int(4350 / 4)
imageHeight = int(2705 / 4)

# infile = 'Grad-WashU.jpg'

im = Image.new("RGB", (imageWidth,imageHeight), color=(227, 7, 14))

barMargin = 35
barWeight = 25
barHorizontalLength = imageWidth * 0.4
barVerticalLength = imageHeight * 0.35

draw = ImageDraw.Draw(im)

draw.rectangle([barMargin, barMargin, barHorizontalLength, barMargin + barWeight], fill=(255,255,255))
draw.rectangle([barMargin, barMargin, barMargin + barWeight, barVerticalLength], fill=(255,255,255))

draw.rectangle([imageWidth - barMargin - barHorizontalLength, imageHeight - barMargin - barWeight, imageWidth - barMargin, imageHeight - barMargin], fill=(255,255,255))
draw.rectangle([imageWidth - barMargin, imageHeight - barMargin, imageWidth - barMargin - barWeight, imageHeight - barWeight - barVerticalLength], fill=(255,255,255))

font = ImageFont.truetype("fonts/Georgia.ttf", size=72)
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore"

quote_lines = text_wrap(text, font, (imageWidth - 6 * barMargin))

line_height = font.getsize('hg')[1]

x = 3 * barMargin
y = 2.5 * barMargin

for line in quote_lines:
    draw.text((x,y), line, fill=(255,255,255), font=font)
    
    y = y + line_height


font = ImageFont.truetype("fonts/Georgia.ttf", size=50)

quote_author = "Emma Baker, Editor-in-Chief"
quote_author = "-" + quote_author

quote_author_size = font.getsize(quote_author)

draw.text(((imageWidth - (3 * barMargin) - quote_author_size[0]), (imageHeight - (2.5 * barMargin) - quote_author_size[1])), quote_author, font=font)

# textBoxMaxSize = (3 * barMargin, 2.5 * barMargin, imageWidth - (3 * barMargin), imageHeight * 0.75)
# draw.rectangle([textBoxMaxSize[0], textBoxMaxSize[1], textBoxMaxSize[2], textBoxMaxSize[3]], fill=(255,255,255))
# draw.multiline_text((3 * barMargin, 2.5 * barMargin), "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore", font=font, fill=(255,255,255))

im.save("output/test.png", "PNG")
