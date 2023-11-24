from settings import *

def replace(char_aliases, char_to_replace, replace_with):
	for type, chars_of_type in char_aliases.items():
		try:
			index = chars_of_type.index(char_to_replace)
			if index > 0:
				char_aliases[type][index] = replace_with
				return
		except:
			pass


def reorder(chars, char_aliases):
	for key in chars:
		sorted_pairs = sorted(zip(char_aliases[key], chars[key]), key=lambda x: x[0])
		char_aliases[key], chars[key] = zip(*sorted_pairs)
