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
				if self.half:
					self.renderer = sr_player_half
				else:
					self.renderer = sr_player_full
			elif self.type == 'teleporter':
				self.renderer = sr_teleporter
		
		self.renderer(self, screen, images, rc)
		

def sr_player_full(sprite, screen, images, rc):
	x = sprite.x - 16
	y = sprite.y - 64
	$image_blit(screen, images['sprites/mc/s0_alt'], x, y)

def sr_player_half(sprite, screen, images, rc):
	x = sprite.x - 8
	y = sprite.y - 32
	$image_blit(screen, images['sprites/mc_half/s0_alt'], x, y)

def sr_teleporter(sprite, screen, images, rc):
	key = 'teleporter/frame' + $str($int(rc / 5) % 3 + 1)
	img = images[key]
	$image_blit(screen, img, sprite.x - 16, sprite.y - 64)