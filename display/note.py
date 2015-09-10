import sys
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time
from EPD import EPD

WHITE = 1
BLACK = 0

possible_fonts = [
    '/usr/share/fonts/TTF/FreeSerif.ttf'                        # Arch
]

italic = "/usr/share/fonts/TTF/FreeSerifItalic.ttf"

FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break
if '' == FONT_FILE:
    raise 'no font file found'

FONT_SIZE = 30
MAX_START = 0xffff

def wrap_text(draw, text, fontFile, width, height):
    size = 120
    while True:
        (success, lines, font) = fit_size(draw, text, fontFile, size, width, height)
        size = size - 1
	if success or size < 1:
	    break      	
    return (lines, font, size)

def fit_size(draw, text, fontFile, size, width, height):
    tokens = text.split()
    tokens.reverse()
    font = ImageFont.truetype(fontFile, size)
    lines = []
    line = []
    while len(tokens) > 0:
	line = []
	while len(tokens) > 0:
	    line.append(tokens.pop())
	    if draw.textsize(' '.join(line), font)[0] > width:
	        if len(line) > 1:
	   	    tokens.append(line.pop())
		    lines.append(' '.join(line))
		    break
	        else:
	      	    return (False, lines, font)
    if (len(line) > 0): 
	lines.append(' '.join(line))
    if len(lines) * size > height:
	return (False, lines, font)
    else: 
 	return (True, lines, font)
    

def main(argv):
    epd = EPD()
    text(epd)

def text(epd):
    image = Image.new('1', epd.size, WHITE)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    draw.rectangle((0, 0, width, height), fill=WHITE, outline=WHITE)
    (lines, font, size) = wrap_text(draw, ' '.join(sys.stdin), FONT_FILE, width, height - 40)
    pos = 0
    print('rendering text')
    for line in lines:
    	draw.text((0, pos), line, fill=BLACK, font=font)
	print(line)
	pos += size
    draw.text((5, pos+10), ' - ' + sys.argv[1], fill=BLACK, font=ImageFont.truetype(italic, 30))
    epd.display(image)
    epd.update()

if "__main__" == __name__:
    if len(sys.argv) < 2:
        sys.exit('usage: {p:s} '.format(p=sys.argv[0]))
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
