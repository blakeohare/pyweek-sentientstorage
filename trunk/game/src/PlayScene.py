CURSOR_WALK = 0
CURSOR_LOOK = 1
CURSOR_HAND = 2
CURSOR_TALK = 3
CURSOR_ITEM = 5

class PlayScene:
	def __init__(self, area_id, game_log):
		self.next = self
		self.canvas = WalkingSurface(area_id, game_log)
		self.cursor = CURSOR_WALK
		self.cursor_item = None
		self.active_item = None
	
	def update(self, events):
		actions = []
		next_scene = None
		for ev in events:
			if ev.type == 'keydown':
				if self.canvas.type == 'WalkingSurface':
					if ev.key == 'c':
						self.canvas.toggle_block_show()
					elif ev.key == 'l':
						self.canvas.toggle_look_show()
			elif ev.type == 'mouseleftdown' or ev.type == 'mouserightdown':
				x = ev.x
				y = ev.y
				if y < 208:
					if self.cursor == CURSOR_WALK or ev.type == 'mouserightdown':
						self.canvas.click_walk(x, y)
					elif self.cursor == CURSOR_LOOK:
						self.canvas.click_look(x, y, self)
					elif self.cursor == CURSOR_HAND:
						self.canvas.click_hand(x, y)
					elif self.cursor == CURSOR_TALK:
						self.canvas.click_talk(x, y)
					elif self.cursor == CURSOR_ITEM:
						if self.cursor_item != None:
							self.canvas.click_item(x, y, self.cursor_item)
				elif ev.type == 'mouseleftdown': # and y >= 208
					y -= 208
					if x < 32:
						if x < 16:
							if y < 16:
								self.cursor = CURSOR_WALK
							else:
								self.cursor = CURSOR_LOOK
						else:
							if y < 16:
								self.cursor = CURSOR_HAND
							else:
								self.cursor = CURSOR_TALK
					elif x < 64:
						self.cursor = CURSOR_ITEM
						if self.active_item == None:
							self.invoke_inventory()
						else:
							self.cursor_item = self.active_item
					elif x < 96:
						self.invoke_inventory()
					elif x > 320 - 32:
						self.invoke_options()
							
		self.canvas.update()
		next_scene = self.canvas.next_scene
		if next_scene != None:
			self.canvas.next_scene = None
			self.next = next_scene
	
	def invoke_inventory(self):
		# TODO: set self.active_item to a string
		pass
	
	def invoke_options(self):
		pass
	
	def render(self, screen, images, rc):
		self.canvas.render(screen, images, rc)
		$image_blit(screen, images['menus/wood_texture'], 0, 208)
		$image_blit(screen, images['menus/buttons'], 0, 208)
		$image_blit(screen, images['menus/item'], 32, 208)
		$image_blit(screen, images['menus/inventory'], 64, 208)
		$image_blit(screen, images['menus/options'], 288, 208)