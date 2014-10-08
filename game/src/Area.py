class Area:
	def __init__(self, name):
		self.id = name
		self.sprites = []
		self.sorted_sprites = None
		self.sprites_by_layers = None
		self.parse_level_file(name)
	
	def initialize_player(self, from_area):
		if from_area == None:
			coords = self.start_point
		else:
			coords = self.start_froms[from_area]
		
		player = Sprite('player', coords[0], coords[1])
		$list_add(self.sprites, player)
		self.player = player
		return player
	
	def parse_level_file(self, name):
		level = read_file('levels/' + name + '.txt')
		rows = $string_split(level, '\n')
		backgrounds_by_id = {}
		background_ids = []
		blocks = []
		region_ids = []
		look_data = {}
		self.layer_images = []
		self.layer_y = []
		start_froms = {}
		start = (0, 0)
		doors = []
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
				elif key == 'STARTFROM':
					from_area = $string_trim(parts[1])
					coords = $string_split(parts[2], ',')
					x = $parse_int($string_trim(coords[0]))
					y = $parse_int($string_trim(coords[1]))
					start_froms[from_area] = (x, y)
				elif key == 'BLOCK':
					data = $string_split(parts[1], ',')
					x = $parse_int($string_trim(data[0]))
					y = $parse_int($string_trim(data[1]))
					width = $parse_int($string_trim(data[2]))
					height = $parse_int($string_trim(data[3]))
					$list_add(blocks, (x, y, x + width, y + height))
				elif key == 'REGION_ID':
					region_id = $string_trim(parts[1])
					coords = $string_split(parts[2], ',')
					x = $parse_int($string_trim(coords[0]))
					y = $parse_int($string_trim(coords[1]))
					width = $parse_int($string_trim(coords[2]))
					height = $parse_int($string_trim(coords[3]))
					$list_add(region_ids, (x, y, width + x, height + y, region_id))
				elif key == 'LOOKY':
					region_id = $string_trim(parts[1])
					sentence = parts[2]
					for i in range(3, $list_length(parts)):
						sentence += ':' + parts[i]
					sentence = $string_split($string_trim(sentence), '|')
					look_data[region_id] = (sentence, None)
				elif key == 'DOOR':
					goes_to = $string_trim(parts[1])
					coords = $string_split(parts[2], ',')
					x = $parse_int($string_trim(coords[0]))
					y = $parse_int($string_trim(coords[1]))
					width = $parse_int($string_trim(coords[2]))
					height = $parse_int($string_trim(coords[3]))
					$list_add(doors, (x, y, width + x, height + y, goes_to))
		
		for bgid in background_ids:
			bg_data = backgrounds_by_id[bgid]
			$list_add(self.layer_images, bg_data[0])
			$list_add(self.layer_y, bg_data[1])
		
		self.start_point = start
		self.start_froms = start_froms
		self.blocks = blocks
		self.region_ids = region_ids
		self.look_data = look_data
		self.doors = doors
	
	def update(self, counter, walk_scene):
		new_sprites = []
		for sprite in self.sprites:
			sprite.update(self)
			if not sprite.dead:
				$list_add(new_sprites, sprite)
		self.sprites = new_sprites
		
		door_value = self.get_door(self.player.x, self.player.y)
		if door_value != None:
			walk_scene.switch_area(door_value)
	
	def get_door(self, x, y):
		for door in self.doors:
			if x >= door[0] and x <= door[2] and y >= door[1] and y <= door[3]:
				return door[4]
		return None
	
	def render(self, screen, images, rc, show_blocks, show_look):
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
		
		if rc % 2 == 0:
			if show_blocks:
				for block in self.blocks:
					$draw_rectangle(screen, block[0], block[1], block[2] - block[0], block[3] - block[1], 0, 0, 255)
			elif show_look:
				for region in self.region_ids:
					left = region[0]
					width = region[2] - region[0]
					top = region[1]
					height = region[3] - region[1]
					$draw_rectangle(screen, left, top, width, height, 0, 128, 0)
					$draw_rectangle(screen, left + 1, top + 1, width - 2, height - 2, 0, 255, 0)
	
	def sort_sprites(self):
		new_list = []
		for sprite in self.sprites:
			$list_add(new_list, sprite)
		
		$list_shuffle(new_list)
		return self.qsort(new_list)
	
	def get_region_id(self, x, y):
		for region in self.region_ids:
			if x < region[2] and x > region[0] and y > region[1] and y < region[3]:
				return region[4]
		return None
		
	def get_look_data(self, region_id):
		return $dictionary_get_with_default(self.look_data, region_id, None)
	
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
	
	