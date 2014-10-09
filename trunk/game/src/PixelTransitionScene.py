_pixel_transition = []
TRANSITION_DURATION = 40

class PixelTransitionScene:
	def __init__(self, from_scene, to_scene):
		self.from_scene = from_scene
		self.to_scene = to_scene
		self.next = self
		self.counter = 0
		self.pixels = self.initialize_pixels()
		
	
	def initialize_pixels(self):
		if $list_length(_pixel_transition) == 0:
			for y in range(60):
				for x in range(80):
					$list_add(_pixel_transition, (x * 4, y * 4))
			$list_shuffle(_pixel_transition)
		return _pixel_transition
	
	def update(self, events):
		self.counter += 1
		if self.counter == TRANSITION_DURATION:
			self.next = self.to_scene
		elif self.to_scene == None and self.counter > TRANSITION_DURATION / 2:
			self.next = None
			
	
	def render(self, screen, images, rc, is_primary):
		$screen_fill(screen, 0, 0, 0)
		mid = $int(TRANSITION_DURATION / 2)
		if self.counter < mid:
			progress = 1.0 * self.counter / mid
			self.from_scene.render(screen, images, rc, False)
		elif self.to_scene != None:
			progress = 1.0 - 1.0 * (self.counter - mid) / mid
			self.to_scene.render(screen, images, rc, False)
		else:
			return
			
		pixels = self.pixels
		total = $list_length(pixels)
		num = $int(progress * total)
		
		for i in range(num):
			pos = pixels[i]
			$draw_rectangle(screen, pos[0], pos[1], 4, 4, 0, 0, 0)
		
		render_cursor('waity', None, screen, images)
		
	
		