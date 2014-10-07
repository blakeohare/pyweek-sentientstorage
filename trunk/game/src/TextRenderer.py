_TEXT_LOOKUP = [None, None]
_CHARS_TO_KEYS = {
	'A': 'ua',
	'B': 'ub',
	'C': 'uc',
	'D': 'ud',
	'E': 'ue',
	'F': 'uf',
	'G': 'ug',
	'H': 'uh',
	'I': 'ui',
	'J': 'uj',
	'K': 'uk',
	'L': 'ul',
	'M': 'um',
	'N': 'un',
	'O': 'uo',
	'P': 'up',
	'Q': 'uq',
	'R': 'ur',
	'S': 'us',
	'T': 'ut',
	'U': 'uu',
	'V': 'uv',
	'W': 'uw',
	'X': 'ux',
	'Y': 'uy',
	'Z': 'uz',
	'a': 'la',
	'b': 'lb',
	'c': 'lc',
	'd': 'ld',
	'e': 'le',
	'f': 'lf',
	'g': 'lg',
	'h': 'lh',
	'i': 'li',
	'j': 'lj',
	'k': 'lk',
	'l': 'll',
	'm': 'lm',
	'n': 'ln',
	'o': 'lo',
	'p': 'lp',
	'q': 'lq',
	'r': 'lr',
	's': 'ls',
	't': 'lt',
	'u': 'lu',
	'v': 'lv',
	'y': 'lw',
	'x': 'lx',
	'y': 'ly',
	'z': 'lz',
	'.': 'period',
	',': 'comma',
	'/': 'slash',
	'\\': 'backslash',
	'?': 'ques',
	'!': 'bang',
	'@': 'at',
	'|': 'pipe',
	'<': 'less',
	'>': 'greater',
	'[': 'openbrack',
	']': 'closebrack',
	'{': 'openbrace',
	'}': 'closebrace',
	'(': 'openparen',
	')': 'closeparen',
	'-': 'hyphen',
	'=': 'equals',
	'_': 'underscore',
	'+': 'plus',
	'*': 'asterisk',
	'&': 'ampersand',
	':': 'colon',
	';': 'semicolon',
	"'": 'apos',
	'"': 'quote'
}

def draw_text(screen, images, x, y, text):
	if _TEXT_LOOKUP[0] == None:
		initialize_text_lookup(images)
	lookup = _TEXT_LOOKUP[0]
	widths = _TEXT_LOOKUP[1]
	original_x = x
	length = $string_length(text)
	images = []
	xs = []
	for i in range(length):
		c = text[i]
		if c == ' ':
			x += 6
		else:
			img = $dictionary_get_with_default(lookup, c, None)
			if img == None:
				img = lookup['?']
				width = widths['?']
			else:
				width = widths[c]
			$list_add(images, img)
			$list_add(xs, x)

			x += width + 1
		
	if $list_length(images) > 0:
		$draw_rectangle(screen, original_x, y, x - original_x, $image_height(images[0]), 200, 200, 230)
	
	for i in range($list_length(xs)):
		x = xs[i]
		img = images[i]
		$image_blit(screen, img, x, y)


def initialize_text_lookup(images):
	lookup = {}
	widths = {}
	for key in $dictionary_keys(_CHARS_TO_KEYS):
		img  = images['font/' + _CHARS_TO_KEYS[key]]
		lookup[key] = img
		widths[key] = $image_width(img)
	_TEXT_LOOKUP[0] = lookup
	_TEXT_LOOKUP[1] = widths
	