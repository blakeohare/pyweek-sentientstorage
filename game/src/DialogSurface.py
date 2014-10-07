TEXT_BG = (200, 200, 230)

class DialogSurface:
	def __init__(self, data, previous_surface, post_dialog_handler):
		self.type = 'DialogSurface'
		self.bg = previous_surface
		self.data = data
		self.next = self
		self.ok = None
		self.pdh = post_dialog_handler
	
	def click(self, x, y):
		if self.ok != None:
			if x > self.ok[0] and x < self.ok[2] and y > self.ok[1] and y < self.ok[3]:
				self.next = self.bg
				self.bg.next = self.bg
				if self.pdh != None:
					self.pdh(self.bg)
	
	def click_walk(self, x, y):
		self.click(x, y)
	def click_hand(self, x, y):
		self.click(x, y)
	def click_look(self, x, y):
		self.click(x, y)
	def click_talk(self, x, y):
		self.click(x, y)
	def click_item(self, x, y, item):
		self.click(x, y)
	
	def update(self):
		pass
	
	def render(self, screen, images, rc):
		self.bg.render(screen, images, rc)
		self.render_real(screen, images)
	
	def render_cursor(self, type, item, screen, images):
		render_cursor('pointy', None, screen, images)
	
	def render_real(self, screen, images):
		text = self.data
		height = $list_length(text) * 15 + 35
		left = 60
		y = 120 - $int(height / 2)
		width = 200
		bottom = y + height
		
		$draw_rectangle(screen, left, y, width, height, TEXT_BG[0], TEXT_BG[1], TEXT_BG[2])
		$draw_rectangle(screen, left + 1, y + 1, width - 2, height - 2, $int(TEXT_BG[0] / 2), $int(TEXT_BG[1] / 2), $int(TEXT_BG[2] / 2))
		$draw_rectangle(screen, left + 2, y + 2, width - 4, height - 4, TEXT_BG[0], TEXT_BG[1], TEXT_BG[2])
		x = left + 5
		y = y + 5
		for i in range($list_length(text)):
			draw_text(screen, images, x, y, text[i])
			y += 15
		
		bwidth = 60
		bleft = left + $int(width / 2) - $int(bwidth / 2)
		btop = bottom - 20
		okbutton = images['menus/ok']
		$image_blit(screen, okbutton, bleft, btop)
		self.ok = (bleft, btop, bleft + $image_width(okbutton), btop + $image_height(okbutton))