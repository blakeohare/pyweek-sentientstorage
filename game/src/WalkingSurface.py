class WalkingSurface:
	def __init__(self, area_id, game_log):
		self.type = 'WalkingSurface'
		self.area = Area(area_id)
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
		$print('touch ' + $str(x) + ', ' + $str(y))
	
	def click_look(self, x, y):
		look_data = self.area.get_look_data(x, y)
		if look_data != None:
			self.next = DialogSurface(look_data[0], self)
	
	def click_talk(self, x, y):
		$print('talk to ' + $str(x) + ', ' + $str(y))
	
	def click_item(self, x, y, item):
		$print(item + ' at ' + $str(x) + ', ' + $str(y))
	
	def update(self):
		self.area.update(self.counter)
		self.counter += 1
	
	def toggle_block_show(self):
		self.block_show = not self.block_show
	
	def toggle_look_show(self):
		self.look_show = not self.look_show
	
	def render(self, screen, images, rc):
		self.area.render(screen, images, rc, self.block_show, self.look_show)