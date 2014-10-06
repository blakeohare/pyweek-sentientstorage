class PlayScene:
	def __init__(self, level, game_log):
		self.next = self
		self.level = level
		self.area = Area(level)
		from_area = game_log.get_string('from_area', None)
		self.area.initialize_player(from_area)
	
	def update(self, events):
		pass
	
	def render(self, screen, images, rc):
		
		self.area.render(screen, images, rc)
		$image_blit(screen, images['menus/wood_texture'], 0, 208)
		$image_blit(screen, images['menus/buttons'], 0, 208)
		$image_blit(screen, images['menus/item'], 32, 208)
		$image_blit(screen, images['menus/inventory'], 64, 208)
		$image_blit(screen, images['menus/options'], 288, 208)