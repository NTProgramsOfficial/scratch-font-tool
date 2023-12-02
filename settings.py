#### After setting up, run using:
# pip install svgwrite fonttools
# python main.py

# Font files (could be in a different directory)
# MUST CHANGE IF YOU DON'T WANT THESE FONTS
font_paths = [
	"Ubuntu-Regular.ttf",
]

# Name (or path) of the char-widths output file
charwidths_path = "charwidths.txt"

# Name (or path) of the folder to place the costumes in
costumes_path = "chars"

# Subfolders for the different costumes
# and the actual characters to generate
chars = {
	"uppercase": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
	"everything-else": list(" abcdefghijklmnopqrstuvwxyz0123456789-_.,!:'?()"),
}

# Ascender height in pixels
char_height = 8

# Number of subpixel steps (must be odd)
steps = 3

import copy                             # IGNORE
from settings_helper import *           # IGNORE
char_aliases = copy.deepcopy(chars)     # IGNORE

# Alternative costume names for certain characters
# to resolve file-name conflicts
replace(char_aliases, '.', 'dot')
replace(char_aliases, ':', 'colon')

reorder(chars, char_aliases)    # IGNORE

#### After setting up, run using:
# pip install svgwrite fonttools
# python main.py