class WalkingSurface:
	def __init__(self, area_id, game_log):
		self.type = 'WalkingSurface'
		self.log = game_log
		self.area = Area(area_id, game_log)
		from_area = game_log.get_string('current_area', None)
		game_log.set_string('current_area', area_id)
		self.player = self.area.initialize_player(from_area)
		self.counter = 0
		self.block_show = False
		self.look_show = False
		self.next = self
		self.timeouts = []
		
	
	def click_walk(self, x, y):
		self.player.set_waypoint(x, y)
	
	def click_hand(self, x, y):
		if self.area.id == 'misc4':
			if x > 31 and x < 120 and y > 77 and y < 194:
				if self.area.player.y > 118:
					if self.log.get_int('HAS_RUBBERBAND', 0) == 2:
						# I don't know why this isn't working the normal way
						pt_misc_hurl_self(self, self.area, self.log, self.area.get_sprite_by_type('rubberband2'), 0)
						return
		region = self.area.get_region_id(x, y)
		if region != None:
			perform_touchy(self, self.area, region, self.log, x, y)
		else:
			sprite = self.area.get_sprite_at(x, y)
			if sprite != None:
				if self.area.id == 'games2' and sprite.type != 'house' and sprite.type != 'getoutofjail' and sprite.type != 'photo4':
					return
				perform_touchy_sprite(self, self.area, sprite, self.log)
							
	
	def click_look(self, x, y):
		sprite = self.area.get_sprite_at(x, y)
		hit = False
		if sprite != None:
			hit = sprite_looky_talky(self, sprite, True)
		
		if not hit:
			# hack
			region = self.area.get_region_id(x, y)
			if self.area.id == 'attic' and region == 'train_box':
				if self.log.get_int('TRAIN_ARRANGE_READY', 0) == 1:
					if self.log.get_int('TRAIN_FIXED', 0) == 0:
						self.invoke_dialog([
							"Alex attempts to fix the train",
							"tracks while carefully avoiding",
							"the sides of the box so he doesn't",
							"get sucked in."], track_arrange_init, [])
						return
			if region != None:
				look_data = self.area.get_look_data(region)
				if look_data != None:
					self.invoke_dialog(look_data[0], None, None)
	
	def click_talk(self, x, y):
		sprite = self.area.get_sprite_at(x, y)
		if sprite != None:
			sprite_looky_talky(self, sprite, False)
	
	def click_item(self, x, y, item):
		if item == None: return
		if self.area.id == 'misc1':
			if x > 186 and x < 227 and y > 74 and y < 117:
				if self.log.get_int('HAS_GLUE', 0) == 1:
					pt_misc_give_glue(self, self.area, self.log)
		region = self.area.get_region_id(x, y)
		sprite = self.area.get_sprite_at(x, y)
		apply_item(self, self.area, self.area.id, item, sprite, region)
	
	def update(self):
		self.area.update(self.counter, self)
		
		if self.area.id == 'legos2' and self.log.get_int('LEGO_STATE', 0) == 0:
			if self.counter == 0:
				self.invoke_dialog([
					"WHAT? How did you get past our",
					"wall!?",
					"This is a breach in our security.",
					"And of course we can't blame ",
					"ourselves. So we blame you. You",
					"are hereby sentenced to death."], joust1b, None)
			elif self.counter == 4:
				self.area.get_sprite_by_type('legohack').dead = True
				self.area.player.y = -500
			elif self.counter == 5:
				self.invoke_dialog([
					"King: Death by joust!",
					"Should you survive, then I shall",
					"let you live."], joust2b, None)
			
		new_timeouts = []
		for timeout in self.timeouts:
			t = timeout[0] - 1
			if t <= 0:
				fun = timeout[1]
				args = timeout[2]
				fun(self, args)
			else:
				timeout[0] = t
				$list_add(new_timeouts, timeout)
		self.timeouts = new_timeouts
		
		self.counter += 1
	
	def toggle_block_show(self):
		self.block_show = not self.block_show
	
	def toggle_look_show(self):
		self.look_show = not self.look_show
	
	def render(self, screen, images, rc):
		self.area.render(screen, images, rc, self.block_show, self.look_show)
	
	def render_cursor(self, cursor_mode, active_item, screen, images):
		if cursor_mode == CURSOR_WALK:
			render_cursor('walky', None, screen, images)
		elif cursor_mode == CURSOR_LOOK:
			render_cursor('looky', None, screen, images)
		elif cursor_mode == CURSOR_HAND:
			render_cursor('touchy', None, screen, images)
		elif cursor_mode == CURSOR_TALK:
			render_cursor('talky', None, screen, images)
		elif cursor_mode == CURSOR_ITEM:
			# TODO: show the item
			render_cursor('pointy', active_item, screen, images)
		else:
			render_cursor('pointy', None, screen, images)
			
	
	def switch_area(self, target_area):
		new_area = Area(target_area, self.log)
		self.log.set_string('current_area', target_area)
		self.player = new_area.initialize_player(self.area.id)
		self.counter = 0
		self.area = new_area
	
	def invoke_dialog(self, text, post_dialog_handler, args):
		self.next = DialogSurface(text, self, post_dialog_handler, args)
		
	