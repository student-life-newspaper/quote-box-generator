import os, sys
from PIL import Image, ImageDraw, ImageFont

imageWidth = 630
imageHeight = 350

# infile = 'Grad-WashU.jpg'

im = Image.new("RGB", (imageWidth,imageHeight), color=(227, 7, 14))

barMargin = 20
barWeight = 15
barHorizontalLength = imageWidth * 0.4
barVerticalLength = imageHeight * 0.35

draw = ImageDraw.Draw(im)

draw.rectangle([barMargin, barMargin, barHorizontalLength, barMargin + barWeight], fill=(255,255,255))
draw.rectangle([barMargin, barMargin, barMargin + barWeight, barVerticalLength], fill=(255,255,255))

draw.rectangle([imageWidth - barMargin - barHorizontalLength, imageHeight - barMargin - barWeight, imageWidth - barMargin, imageHeight - barMargin], fill=(255,255,255))
draw.rectangle([imageWidth - barMargin, imageHeight - barMargin, imageWidth - barMargin - barWeight, imageHeight - barWeight - barVerticalLength], fill=(255,255,255))

font = ImageFont.truetype("fonts/Georgia.ttf", size=80)
draw.multiline_text((2* barMargin, 2* barMargin), "This is a test. Hi Emma.",font=font)

im.save("output/test.png", "PNG")
