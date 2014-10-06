class WalkingSurface:
	def __init__(self, area_id, game_log):
		self.area = Area(area_id)
		from_area = game_log.get_string('current_area', None)
		game_log.set_string('current_area', area_id)
		self.player = self.area.initialize_player(from_area)
		self.counter = 0
	
	def click_walk(self, x, y):
		self.player.set_waypoint(x, y)
	
	def click_hand(self, x, y):
		$print('touch ' + $str(x) + ', ' + $str(y))
	
	def click_look(self, x, y):
		$print('look at ' + $str(x) + ', ' + $str(y))
	
	def click_talk(self, x, y):
		$print('talk to ' + $str(x) + ', ' + $str(y))
	
	def click_item(self, x, y, item):
		$print(item + ' at ' + $str(x) + ', ' + $str(y))
	
	def update(self):
		self.area.update(self.counter)
		self.counter += 1
	
	def render(self, screen, images, rc):
		self.area.render(screen, images, rc)