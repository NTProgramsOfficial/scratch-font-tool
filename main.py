#### View settings.py for options before running

###############################################################################

import os
import shutil
import svgwrite
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from settings import *
from settings_helper import *
from prompt import confirm

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
	costume = svgwrite.Drawing(costume_path, profile='tiny', size=('480px', '360px'))
	costume.viewbox(0, 0, 480, 360)
	transform_size = char_height / units_per_em
	costume.add(costume.rect(insert=(240 - 0.25 * char_height - 2, 180 - 0.75 * char_height - 2),
							size=(char_height + 4, char_height + 4),
							fill='green',
							opacity='0'))
	costume.add(costume.path(d=svg_char_path,
							fill='red',
							transform=f"translate({240 + step / steps}, 180) scale({transform_size}, {-transform_size})"))
	costume.save()


def get_glyph(char, glyph_set):
    return glyph_set[f"uni{f'{ord(char):#0{6}x}'[2:].upper()}"]


def get_svg_char_path(glyph):
	pen = SVGPathPen(None)
	glyph.draw(pen)
	return pen.getCommands()


def get_costume_path(char_type, char_number, font_number, step):
	char_alias = char_aliases[char_type][char_number]
	return os.path.join(costumes_path, char_type, f'{font_number}_{char_alias}{step if steps > 1 else ""}.svg')


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
