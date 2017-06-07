def track_arrange_init(scene, args):
	scene.next = TracksArrange(scene)

class TracksArrange:
	def __init__(self, bg):
		self.next = self
		self.type = 'TracksArrange'
		self.bg = bg
		self.bg.next = bg
		self.pos = [0, 0]
		self.order = [
			'track5', 'track6', 'track4', 'track3', 'track2', 'track7', 'track1'
		]
		self.solution = {
			'track1': (89, 148),
			'track2': (41, 123), 
			'track3': (95, 83),
			'track4': (134, 55),
			'track5': (88, 35),
			'track6': (41, 54),
			'track7': (143, 126)
		}
		self.pieces = {
			'track1': [194, 166, 0, 0, 0, 0],
			'track2': [240, 110, 0, 0, 0, 0], 
			'track3': [153, 66, 0, 0, 0, 0],
			'track4': [232, 48, 0, 0, 0, 0],
			'track5': [114, 112, 0, 0, 0, 0],
			'track6': [98, 161, 0, 0, 0, 0],
			'track7': [88, 59, 0, 0, 0, 0]
		}
		self.neighbors = {
			'track1': ['track2', 'track7'],
			'track2': ['track1', 'track3'],
			'track3': ['track2', 'track7', 'track4', 'track6'],
			'track4': ['track3', 'track5'],
			'track5': ['track4', 'track6'],
			'track6': ['track5', 'track3'],
			'track7': ['track3', 'track1']
		}
		self.holding = None
		self.regions = {}
		
	def update(self):
		tnew_pos = get_mouse_position()
		new_pos = [tnew_pos[0], tnew_pos[1]]
		dx = new_pos[0] - self.pos[0]
		dy = new_pos[1] - self.pos[1]
		self.pos = new_pos
		if self.holding != None:
			self.pieces[self.holding][0] += dx
			self.pieces[self.holding][1] += dy
	
	def click_hand(self, x, y): self.click(x, y)
	def click_walk(self, x, y): self.click(x, y)
	def click_look(self, x, y): self.click(x, y)
	def click_talk(self, x, y): self.click(x, y)
	def click_item(self, x, y, item): self.click(x, y)
	
	def click(self, x, y):
		if x < 10 or x > 310 or y < 10 or y > 198:
			self.next = self.bg
			self.next.next = self.next
		
		if self.holding != None:
			dropped = self.holding
			self.holding = None
			for neighbor in self.neighbors[dropped]:
				dropped_real_coords = self.pieces[dropped]
				n_real_coords = self.pieces[neighbor]
				rdx = dropped_real_coords[0] - n_real_coords[0]
				rdy = dropped_real_coords[1] - n_real_coords[1]
				
				dropped_final_coords = self.solution[dropped]
				n_final_coords = self.solution[neighbor]
				fdx = dropped_final_coords[0] - n_final_coords[0]
				fdy = dropped_final_coords[1] - n_final_coords[1]
				
				dx = rdx - fdx
				dy = rdy - fdy
				
				if dx ** 2 + dy ** 2 < 16:
					for i in (0, 1):
						self.pieces[dropped][i] = self.solution[dropped][i] - self.solution[neighbor][i] + self.pieces[neighbor][i]
					break
			
			for key in $dictionary_keys(self.pieces):
				for neighbor in self.neighbors[key]:
					fdx = self.solution[neighbor][0] - self.solution[key][0]
					fdy = self.solution[neighbor][1] - self.solution[key][1]
					
					rdx = self.pieces[neighbor][0] - self.pieces[key][0]
					rdy = self.pieces[neighbor][1] - self.pieces[key][1]
					
					if fdx != rdx or fdy != rdy:
						return
			
			self.next = self.bg
			self.next.next = self.next
			self.next.log.set_int('TRAIN_FIXED', 1)
			self.next.invoke_dialog(["Alex successfully arranges the", "tracks."], None, None)
			
		else:
			for key in $dictionary_keys(self.pieces):
				piece = self.pieces[key]
				if x > piece[2] and x < piece[4] and y > piece[3] and y < piece[5]:
					self.holding = key
					return
		
	
	def render(self, screen, images, rc):
		$draw_rectangle(screen, 0, 0, 320, 208, 60, 30, 0)
		$draw_rectangle(screen, 10, 10, 300, 188, 0, 128, 50)
		for key in self.order:
			x = self.pieces[key][0]
			y = self.pieces[key][1]
			img = images['tracks/' + key]
			width = $image_width(img)
			height = $image_height(img)
			left = x - $int(width / 2)
			top = y - $int(height / 2)
			$image_blit(screen, img, left, top)
			self.pieces[key][2] = left
			self.pieces[key][3] = top
			self.pieces[key][4] = left + width
			self.pieces[key][5] = top + height
			
	
	def render_cursor(self, cursor_mode, active_item, screen, images):
		render_cursor('pointy', None, screen, images)