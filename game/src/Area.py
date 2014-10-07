class Area:
	def __init__(self, name):
		self.id = name
		self.sprites = []
		self.sorted_sprites = None
		self.sprites_by_layers = None
		self.parse_level_file(name)
	
	def initialize_player(self, fromArea):
		if fromArea == None:
			coords = self.start_point
		else:
			pass # TODO: this
		
		player = Sprite('player', coords[0], coords[1])
		$list_add(self.sprites, player)
		return player
	
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
	
	def update(self, counter):
		new_sprites = []
		for sprite in self.sprites:
			sprite.update(self)
			if not sprite.dead:
				$list_add(new_sprites, sprite)
		self.sprites = new_sprites
	
	def render(self, screen, images, rc, show_blocks):
		sprites = self.sort_sprites()
		layer_index = 0
		sprite_index = 0
		layer_count = $list_length(self.layer_y)
		sprite_count = $list_length(sprites)
		while layer_index < layer_count or sprite_index < sprite_count:
			
			if layer_index == layer_count:
				is_sprite = True
			elif sprite_index == sprite_count:
				is_sprite = False
			elif sprites[sprite_index].y < self.layer_y[layer_index]:
				is_sprite = True
			else:
				is_sprite = False
			
			if is_sprite:
				sprites[sprite_index].render(screen, images, rc)
				sprite_index += 1
			else:
				$image_blit(screen, images[self.layer_images[layer_index]], 0, 0)
				layer_index += 1
		if show_blocks and rc % 2 == 0:
			for block in self.blocks:
				$draw_rectangle(screen, block[0], block[1], block[2] - block[0], block[3] - block[1], 0, 0, 255)
	
	def sort_sprites(self):
		new_list = []
		for sprite in self.sprites:
			$list_add(new_list, sprite)
		
		$list_shuffle(new_list)
		return self.qsort(new_list)
	
	def is_passable(self, x, y):
		for block in self.blocks:
			if y <= block[3] and y >= block[1] and x >= block[0] and x <= block[2]:
				return False
		return True
	
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
		output = self.qsort(left) + [pivot] + self.qsort(right)
		return output
	
	