class Area:
	def __init__(self, name):
		self.sprites = []
		self.sprites_by_layers = None
		self.parse_level_file(name)
	
	def initialize_player(self, fromArea):
		if fromArea == None:
			coords = self.start_point
		else:
			pass # TODO: this
	
	def parse_level_file(self, name):
		level = read_file('levels/' + name + '.txt')
		rows = $string_split(level, '\n')
		backgrounds_by_id = {}
		background_ids = []
		blocks = []
		self.layer_images = []
		self.layer_y = []
		start = (0, 0)
		for row in rows:
			trow = $string_trim(row)
			if $string_length(trow) > 0 and trow[0] != '#':
				parts = trow.split(':')
				key = $string_upper($string_trim(parts[0]))
				if key == 'LAYERS':
					for bg in $string_split(parts[1], ','):
						$list_add(background_ids, $string_trim(bg))
				elif key == 'LAYER_DATA':
					bg = $string_trim(parts[1])
					data = $string_split(parts[2], ',')
					image = $string_trim(data[0])
					yboundary = $parse_int(data[1])
					backgrounds_by_id[bg] = (image, yboundary)
				elif key == 'START':
					data = $string_split(parts[1], ',')
					x = $parse_int($string_trim(data[0]))
					y = $parse_int($string_trim(data[1]))
					start = (x, y)
				elif key == 'BLOCK':
					data = $string_split(parts[1], ',')
					x = $parse_int($string_trim(data[0]))
					y = $parse_int($string_trim(data[1]))
					width = $parse_int($string_trim(data[2]))
					height = $parse_int($string_trim(data[3]))
					$list_add(blocks, (x, y, x + width, y + height))
		
		for bgid in background_ids:
			bg_data = backgrounds_by_id[bgid]
			$list_add(self.layer_images, bg_data[0])
			$list_add(self.layer_y, bg_data[1])
		
		self.start_point = start
		self.blocks = blocks
	
	def render(self, screen, images, rc):
		self.sort_sprites()
		for i in range($list_length(self.layer_images)):
			image = self.layer_images[i]
			$image_blit(screen, images[image], 0, 0)
	
	def sort_sprites(self):
		
		$list_shuffle(self.sprites)
		sorted = self.qsort(self.sprites)
		# TODO: bucketing
	
	def qsort(self, items):
		if $list_length(items) < 2: return items
		left = []
		right = []
		pivot = items[0]
		pivot_value = pivot.y * 10000 + pivot.x
		for i in range(1, $list_length(items)):
			sprite = items[i]
			if sprite.y * 10000 + sprite.x < pivot_value:
				$list_add(left, sprite)
			else:
				$list_add(right, sprite)
		output = left + [pivot] + right
		return output
	
	