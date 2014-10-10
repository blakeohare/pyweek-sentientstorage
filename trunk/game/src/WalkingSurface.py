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
	
	def click_walk(self, x, y):
		self.player.set_waypoint(x, y)
	
	def click_hand(self, x, y):
		region = self.area.get_region_id(x, y)
		if region != None:
			perform_touchy(self, self.area, region, self.log)
		else:
			sprite = self.area.get_sprite_at(x, y)
			if sprite != None:
				perform_touchy_sprite(self, self.area, sprite, self.log)
							
	
	def click_look(self, x, y):
		region = self.area.get_region_id(x, y)
		if region != None:
			look_data = self.area.get_look_data(region)
			if look_data != None:
				self.invoke_dialog(look_data[0], None, None)
	
	def click_talk(self, x, y):
		$print('talk to ' + $str(x) + ', ' + $str(y))
	
	def click_item(self, x, y, item):
		if item == None: return
		region = self.area.get_region_id(x, y)
		sprite = self.area.get_sprite_at(x, y)
		apply_item(self, self.area, self.area.id, item, sprite, region)
	
	def update(self):
		self.area.update(self.counter, self)
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
		
	