class Sprite:
	def __init__(self, type, x, y):
		self.type = type
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.waypoints = []
		self.v = 2.0
		self.last_direction = 's'
		self.dead = False
		self.half = False
		self.renderer = None
	
	def update(self, area):
		if $list_length(self.waypoints) > 0:
			wp = self.waypoints[0]
			dx = wp[0] - self.x
			dy = wp[1] - self.y
			dist = (dx ** 2 + dy ** 2) ** .5
			if dist <= self.v:
				self.dx = wp[0] - self.x
				self.dy = wp[1] - self.y
				$list_remove(self.waypoints, 0)
			else:
				self.dx = 1.0 * dx * self.v / dist
				self.dy = 1.0 * dy * self.v / dist
		if self.dx != 0 or self.dy != 0:
			dx = self.dx
			dy = self.dy
			self.last_direction = self.convert_vector_to_direction(dx, dy)
			newx = self.x + dx
			newy = self.y + dy
			if area.is_passable(newx, newy):
				self.x = newx
				self.y = newy
			self.dx = 0
			self.dy = 0
	
	def set_waypoint(self, tx, ty):
		self.waypoints = [(tx, ty)]
	
	def queue_waypoint(self, tx, ty):
		$list_add(self.waypoints, (tx, ty))
	
	def convert_vector_to_direction(self, dx, dy):
		# TODO: this
		return 's'
			
	def render(self, screen, images, rc):
		if self.renderer == None:
			if self.type == 'player':
				if self.scale == 'half': self.renderer = sr_player_half
				elif self.scale == 'double': self.renderer = sr_player_double
				else: self.renderer = sr_player_full
			elif self.type == 'teleporter': self.renderer = sr_teleporter
			elif self.type == 'boot': self.renderer = sr_boot
			elif self.type == 'thimble': self.renderer = sr_thimble
			elif self.type == 'rubberband': self.renderer = sr_rubberband
				
		self.renderer(self, screen, images, rc)

def draw_image_centered(screen, sprite, img):
	w = $image_width(img)
	h = $image_height(img)
	x = sprite.x - $int(w / 2)
	y = sprite.y - h
	$image_blit(screen, img, x, y)
	sprite.last_width = w
	sprite.last_height = h





def sr_rubberband(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/rubberband_ground'])

def sr_thimble(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/thimble'])

def sr_boot(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/boot'])

def sr_player_double(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc_double/s0_alt'])

def sr_player_full(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc/s0_alt'])

def sr_player_half(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc_half/s0_alt'])

def sr_teleporter(sprite, screen, images, rc):
	key = 'teleporter/frame' + $str($int(rc / 5) % 3 + 1)
	draw_image_centered(screen, sprite, images[key])
