#### View settings.py for options before running

###############################################################################

import os
import shutil
from unittest.mock import Base
from svgpathtools import parse_path, wsvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from settings import *
from settings_helper import *
from prompt import confirm

template = open('template.svg', 'r').read().replace('[[]]', f'{char_height * 2}')

if os.path.exists(costumes_path):
	if not confirm(f"'{costumes_path}/' exists. Overwrite? "):
		print("Cancelled.")
		exit()
	shutil.rmtree(costumes_path)

if os.path.exists(charwidths_path):
	if not confirm(f"'{charwidths_path}' exists. Overwrite? "):
		print("Cancelled.")
		exit()
	os.remove(charwidths_path)

os.mkdir(costumes_path)
charwidths = open(charwidths_path, 'w')

def create_costume(svg_char_path, costume_path, units_per_em, step):
	# costume = svgwrite.Drawing(costume_path, profile='tiny', size=(char_height + 4, char_height + 4))
	# costume.viewbox(0, 0, char_height + 4, char_height + 4)
	transform_size = char_height / units_per_em
	# costume.add(costume.rect(insert=(-0.25 * char_height - 2, -0.75 * char_height - 2),
	# 						size=(char_height + 4, char_height + 4),
	# 						fill='green',
	# 						opacity='0'))
	# if svg_char_path != '':
	# 	costume.add(costume.path(d=svg_char_path,
	# 							 fill='red',
	# 							 transform=f"translate({(step + 1) / steps - 0.5}, 0) scale({transform_size}, {-transform_size})"))
	# costume.save()
	with open(costume_path, 'w') as file:
		path = parse_path(svg_char_path).scaled(transform_size, -transform_size, 240 + char_height / 2 + (step + 1) / steps - 0.5 + (180 + char_height) * 1j)
		file.write(template.replace('{{}}', path.d()))
		file.close()


def get_glyph(char, glyph_set):
	# code = f"uni{f'{ord(char):#0{6}x}'[2:].upper()}"
	key = glyph_set.font['cmap'].getBestCmap()[ord(char)]
	return glyph_set[key]
	# if code in glyph_set:
	# 	return glyph_set[code]
	# if char in glyph_set:
	# 	return glyph_set[char]
	


def get_svg_char_path(glyph):
	pen = SVGPathPen(glyph.glyphSet)
	glyph.draw(pen)
	return pen.getCommands()


def get_costume_path(char_type, char_number, font_number, step):
	char_alias = char_aliases[char_type][char_number]
	return os.path.join(costumes_path, char_type, f'{f"{font_number}_" if len(font_paths) > 1 else ""}{char_alias}{step if steps > 1 else ""}.svg')


for char_type in chars:
	os.mkdir(os.path.join(costumes_path, char_type))
	for font_number, font_path in enumerate(font_paths):
		ttfont = TTFont(font_path)
		units_per_em = ttfont['head'].unitsPerEm # type: ignore
		glyph_set = ttfont.getGlyphSet()
		for char_number, char in enumerate(chars[char_type]):
			for step in range(steps):
				glyph = get_glyph(char, glyph_set)
				costume_path = get_costume_path(char_type, char_number, font_number, step)
				svg_char_path = get_svg_char_path(glyph)
				create_costume(svg_char_path, costume_path, units_per_em, step)
			charwidths.write(f'{glyph.width / units_per_em * char_height}\n')
