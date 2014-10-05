class TitleScene:
	def __init__(self):
		self.next = self
		self.x = 0
		self.y = 0
	
	def update(self, events):
		self.x += 2
		self.y += 1
		for ev in events:
			if ev.type == 'quit':
				self.next = None
	
	def render(self, screen, images, rc):
		$screen_fill(screen, 0, 50, 100)
		$image_blit(screen, images['test'], self.x, self.y)
