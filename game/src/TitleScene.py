class TitleScene:
	def __init__(self):
		self.next = self
		self.x = 0
		self.y = 0
	
	def update(self, events):
		self.x += 2
		self.y += 1
		action = None
		for ev in events:
			if ev.type == 'quit':
				self.next = None
			elif ev.type == 'mouseleftdown':
				x = ev.x
				y = ev.y
				if x > 87 and x < 209 and y > 127 and y < 152:
					action = 'new'
				elif x > 87 and x < 209 and y > 158 and y < 187:
					action = 'load'
				elif x > 115 and x < 164 and y > 191 and y < 216:
					action = 'exit'
		
		if action == 'new':
			self.next = PixelTransitionScene(self, PlayScene('attic'))
		elif action == 'load':
			self.next = LoadGameScene(self)
		elif action == 'exit':
			self.next = PixelTransitionScene(self, None)
		
	
	def render(self, screen, images, rc):
		#$screen_fill(screen, 0, 50, 100)
		$image_blit(screen, images['menus/title'], 0, 0)
		
