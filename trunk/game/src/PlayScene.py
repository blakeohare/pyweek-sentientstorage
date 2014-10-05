class PlayScene:
	def __init__(self, level):
		self.next = self
		self.level = level
	
	def update(self, events):
		pass
	
	def render(self, screen, images, rc):
		$screen_fill(screen, 0, 255, 0)