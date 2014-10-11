
MONOPOLY_INDEX = [
	(87, 141),
	(87, 121),
	(109, 106),
	(142, 97),
	(177, 97),
	(210, 106),
	(231, 121),
	(231, 141)
]

ALL_TOKEN_KEYS = ['tophat', 'scottie', 'wheelbarrow', 'racecar', 'horse', 'battleship', 'boot', 'thimble']

class Area:
	def __init__(self, name, log):
		self.id = name
		self.sprites = []
		self.sorted_sprites = None
		self.sprites_by_layers = None
		self.music = None
		self.parse_level_file(name, log)
		self.volume = 1
		self.log = log
		
		tokens = []
		if name == 'games2':
			for token in ALL_TOKEN_KEYS:
				if log.get_int('HAS_' + $string_upper(token), 0) == 2:
					index = log.get_int($string_upper(token) + '_INDEX', 0)
					coords = MONOPOLY_INDEX[index]
					x = coords[0]
					y = coords[1]
					$list_add(self.sprites, Sprite(token, x, y))
					
			
		self.train_go = False
		self.train_counter = 0
		
		if name == 'trains2':
			log.set_int('SAW_NIGHTCLUB', 1)
		
		
	def initialize_player(self, from_area):
		if from_area == None:
			coords = self.start_point
		else:
			coords = self.start_froms[from_area]
		
		player = Sprite('player', coords[0], coords[1])
		player.scale = self.scale
		$list_add(self.sprites, player)
		self.player = player
		return player
	
	def parse_level_file(self, name, log):
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
		scale = 'full'
		teleporter = None
		for row in rows:
			trow = $string_trim(row)
			if $string_length(trow) > 0 and trow[0] != '#':
				while $string_length(trow) > 0 and trow[0] == '<':
					orig_parts = $string_split(trow, '>')
					expr_parts = $string_split($string_split(orig_parts[0], '<')[1], ':')
					expr = expr_parts[0]
					value = $parse_int(expr_parts[1])
					current_value = log.get_int(expr, 0)
					if current_value == value:
						new_trow = orig_parts[1]
						for i in range(2, $list_length(orig_parts)):
							new_trow += '>' + orig_parts[i]
						trow = new_trow
					else:
						trow = 'IGNORE_ME'
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
					triangle_direction = None
					if $list_length(data) > 4:
						triangle_direction = $string_trim($string_upper(data[4]))
					$list_add(blocks, (x, y, x + width, y + height, triangle_direction))
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
				elif key == 'TELEPORTER':
					coords = $string_split(parts[1], ',')
					x = $parse_int($string_trim(coords[0]))
					y = $parse_int($string_trim(coords[1]))
					teleporter = (x, y)
				elif key == 'SCALE':
					value = $string_trim($string_lower(parts[1]))
					if value == 'full' or value == 'half' or value == 'double':
						scale = value
				elif key == 'ADD_SPRITE':
					data = $string_split(parts[1], ',')
					type = $string_trim(data[0])
					x = $parse_int($string_trim(data[1]))
					y = $parse_int($string_trim(data[2]))
					$list_add(self.sprites, Sprite(type, x, y))
				elif key == 'MUSIC':
					self.music = $string_trim(parts[1])
					
		
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
		self.teleporter = teleporter
		self.scale = scale
		if teleporter != None:
			$list_add(self.sprites, Sprite('teleporter', teleporter[0], teleporter[1]))
	
	def remove_block_at(self, x, y):
		found = None
		for i in range($list_length(self.blocks)):
			block = self.blocks[i]
			if block[0] < x and block[1] < y and block[2] > x and block[3] > y:
				found = i
				break
		
		if found != None:
			$list_remove(self.blocks, i)
		
	
	def update(self, counter, walk_scene):
		
		new_sprites = []
		for sprite in self.sprites:
			sprite.update(self)
			if not sprite.dead:
				$list_add(new_sprites, sprite)
		self.sprites = new_sprites
		
		if counter == 1:
			$music_play(self.music)
		
		door_value = self.get_door(self.player.x, self.player.y)
		if door_value != None:
			walk_scene.switch_area(door_value)
			if self.id == 'legos3' and door_value == 'legos2' and self.player.y > 124:
				walk_scene.area.player.x = 179
				walk_scene.area.player.y = 53
			elif self.id == 'legos2' and door_value == 'legos3' and self.player.x > 112:
				walk_scene.area.player.x = 110
				walk_scene.area.player.y = 143
				
			
		if self.teleporter != None:
			tele_dx = self.player.x - self.teleporter[0]
			tele_dy = self.player.y - self.teleporter[1]
			if tele_dx ** 2 + tele_dy ** 2 < 16 ** 2:
				walk_scene.switch_area('attic')
		
		if self.train_go:
			self.train_counter += 1
			for sprite in self.sprites:
				if sprite.type == 'enginewithwheel' or sprite.type == 'traincar':
					sprite.x -= 4
					sprite.y += 1
			if self.train_counter >= 50:
				if self.id == 'trains1':
					walk_scene.switch_area('trains2')
				else:
					walk_scene.switch_area('trains1')
		if counter == 3 and self.id == 'legos1':
			if walk_scene.log.get_int('KNIGHTS_SHPIEL', 0) == 0:
				$list_add(walk_scene.timeouts, [3, knights_shpiel_1, []])
		
		if self.id == 'attic':
			if self.log.get_int('INTRO_SHOWN', 0) == 0:
				self.log.set_int('INTRO_SHOWN', 1)
				cs_attic_intro1(walk_scene)
			elif self.log.get_int('ENDING_SHOWN', 0) == 0:
				total = 0
				for i in range(1, 6):
					total += self.log.get_int('HAS_PHOTO' + $str(i), 0)
				
				if total == 5:
					self.log.set_int('ENDING_SHOWN', 1)
					cs_attic_ending1(walk_scene)
					
		elif self.id == 'misc3':
			dino_state = walk_scene.log.get_int('DINO_STATE', 0)
			if dino_state == 0:
				# T-Rex chases you
				x = self.player.x
				y = self.player.y
				if x > 129 and x < 260 and y > 69 and y <= 115:
					self.player.waypoints = [[253, 177]]
					dino = self.get_sprite_by_type('dino')
					dino.waypoints = [[162, 87]]
					self.player.enforce_waypoint = True
					$list_add(walk_scene.timeouts, [30, dino_retreats, []])
					if walk_scene.log.get_int('DINO_SCARE', 0) == 0:
						walk_scene.log.set_int('DINO_SCARE', 1)
						walk_scene.invoke_dialog([
							"Out of seemingly nowhere, a plastic",
							"T-Rex jumps out of hiding and",
							"chases you away from the cave."], None, None)
			elif dino_state == 1:
				if counter == 1:
					dinos_shpiel_1(walk_scene)
			
	def get_sprite_by_type(self, type):
		for sprite in self.sprites:
			if sprite.type == type:
				return sprite
		return None
	
	def get_sprite_at(self, x, y):
		sprites = self.sorted_sprites
		if sprites == None:
			sprites = self.sprites
		i = $list_length(sprites) - 1
		while i >= 0:
			sprite = sprites[i]
			if sprite.last_width != None:
				width = sprite.last_width
				left = sprite.x - width / 2
				right = left + width
				if left < x and right > x:
					bottom = sprite.y
					top = bottom - sprite.last_height
					if y > top and y < bottom:
						return sprite
			i -= 1
		return None
	
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
			elif sprites[sprite_index].sorty < self.layer_y[layer_index]:
				is_sprite = True
			else:
				is_sprite = False
			
			if is_sprite:
				sprites[sprite_index].render(screen, images, rc)
				sprite_index += 1
			else:
				$image_blit(screen, images[self.layer_images[layer_index]], 0, 0)
				layer_index += 1
		
		if self.id == 'trains2':
			c = $int(rc / 6) % 4
			if c == 0:
				$image_blit(screen, images['backgrounds/trains2-2'], 0, 0)
			elif c == 1 or c == 3:
				$image_blit(screen, images['backgrounds/trains2-3'], 0, 0)
			else:
				$image_blit(screen, images['backgrounds/trains2-4'], 0, 0)
		
		if rc % 2 == 0:
			if show_blocks:
				for block in self.blocks:
					tri = block[4]
					x = block[0]
					y = block[1]
					top = y
					left = x
					width = block[2] - block[0]
					height = block[3] - block[1]
					right = x + width
					bottom = y + height
					
					if tri == None:
						$draw_rectangle(screen, x, y, width, height, 0, 0, 255)
					elif tri == 'TL':
						$draw_triangle(screen, x, y, x, bottom, right, y, 0, 0, 255)
					elif tri == 'TR':
						$draw_triangle(screen, left, top, right, top, right, bottom, 0, 0, 255)
					elif tri == 'BL':
						$draw_triangle(screen, left, top, left, bottom, right, bottom, 0, 0, 255)
					elif tri == 'BR':
						$draw_triangle(screen, left, bottom, right, bottom, right, top, 0, 0, 255)
						
			elif show_look:
				for region in self.region_ids:
					left = region[0]
					width = region[2] - region[0]
					top = region[1]
					height = region[3] - region[1]
					$draw_rectangle(screen, left, top, width, height, 0, 128, 0)
					$draw_rectangle(screen, left + 1, top + 1, width - 2, height - 2, 0, 255, 0)
		if self.id == 'trains3' and self.log.get_int('HAS_WIZARD', 0) == 2:
			c = rc % 6
			if c < 3:
				img = images['backgrounds/strobe1']
			else:
				img = images['backgrounds/strobe2']
			$image_blit(screen, img, 0, 0)
	def sort_sprites(self):
		new_list = []
		for sprite in self.sprites:
			sprite.sorty = sprite.y
			if sprite.type == 'tophat' and self.id == 'trains1':
				sprite.sorty += 9999
			if sprite.type == 'legohack':
				sprite.sorty += 9999999
			$list_add(new_list, sprite)
		
		$list_shuffle(new_list)
		self.sorted_sprites = self.qsort(new_list)
		return self.sorted_sprites
	
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
				tri = block[4]
				if tri == None: return False
				# check triangles
				w = block[2] - block[0]
				h = block[3] - block[1]
				px = 1.0 * (x - block[0]) / w
				py = 1.0 * (y - block[1]) / h
				
				if tri == 'TL':
					if px + py <= 1: return False
				elif tri == 'TR':
					px = 1.0 - px
					if px + py <= 1: return False
				elif tri == 'BR':
					if px + py >= 1: return False
				elif tri == 'BL':
					px = 1.0 - px
					if px + py >= 1: return False
					
				
		return True
	
	def qsort(self, items):
		if $list_length(items) < 2: return items
		left = []
		right = []
		pivot = items[0]
		pivot_value = pivot.sorty * 10000 + pivot.x
		for i in range(1, $list_length(items)):
			sprite = items[i]
			if sprite.sorty * 10000 + sprite.x < pivot_value:
				$list_add(left, sprite)
			else:
				$list_add(right, sprite)
		output = self.qsort(left) + [pivot] + self.qsort(right)
		return output
	
def dino_retreats(scene, args):
	dino = scene.area.get_sprite_by_type('dino')
	dino.waypoints = [[71, 88]]