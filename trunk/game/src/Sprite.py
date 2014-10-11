DIR_VECTORS = {
	's': (0, 1),
	'n': (0, -1),
	'e': (1, 0),
	'w': (-1, 0)
}
DIRS = ('n', 's', 'e', 'w')

class Sprite:
	def __init__(self, type, x, y):
		self.type = type
		self.log = None
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
		self.lifetime = 0
		self.ghost = type == 'ball' or type == 'dino' or type == 'chewedgum' # can pass through things
		self.teething = False
		if type == 'dino':
			self.v = 6.0
		self.enforce_waypoint = False
		self.stretched = False
	
	def specific_update(self, type, area, counter):
		if type == 'mothercar1' or type == 'mothercar2':
			self.dx = $math_sin(self.lifetime * 2 * 3.14159 / 100)
		elif type == 'hippochoke':
			rate = 30
			c = counter % rate
			if c == 0:
				self.dx = -2
			elif c == $int(rate / 2):
				self.dx = 2
		elif type == 'scottie':
			if area.id == 'trains2':
				c = counter % 50
				if c < 25:
					self.dx = -1
				else:
					self.dx = 1
		elif type == 'raver1' or type == 'raver2':
			c = counter % 15
			if c == 2:
				self.dy = -3
			elif c == 7:
				self.dy = 3
				
	def update(self, area):
		self.log = area.log
		self.specific_update(self.type, area, self.lifetime)
		self.lifetime += 1
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
			if area.is_passable(newx, newy) or self.ghost:
				self.x = newx
				self.y = newy
			self.dx = 0
			self.dy = 0
	
	def set_waypoint(self, tx, ty):
		if $list_length(self.waypoints) > 0:
			if self.enforce_waypoints:
				return
		self.enforce_waypoints = False
		self.waypoints = [(tx, ty)]
	
	def queue_waypoint(self, tx, ty):
		$list_add(self.waypoints, (tx, ty))
	
	def convert_vector_to_direction(self, dx, dy):
		if dx == 0:
			if dy < 0:
				return 'n'
			else:
				return 's'
		elif dy == 0:
			if dx < 0:
				return 'w'
			else:
				return 'e'
		
		closest_value = 999999999
		closest_key = 's'
		for d in DIRS:
			vec = DIR_VECTORS[d]
			tdx = vec[0] - dx
			tdy = vec[1] - dy
			dist = tdx * tdx + tdy * tdy
			if dist < closest_value:
				closest_value = dist
				closest_key = d
		return closest_key
			
			
				
			
	def render(self, screen, images, rc):
		if self.renderer == None:
			if self.type == 'player':
				if self.scale == 'half': self.renderer = sr_player_half
				elif self.scale == 'double': self.renderer = sr_player_double
				else: self.renderer = sr_player_full
			else:
				if self.type[0] == 'b':
					if self.type == 'ball': self.renderer = sr_ball
					elif self.type == 'battleship': self.renderer = sr_battleship
					elif self.type == 'bballplayer1': self.renderer = sr_bballplayer1
					elif self.type == 'bballplayer2': self.renderer = sr_bballplayer2
					elif self.type == 'bballplayer3': self.renderer = sr_bballplayer3
					elif self.type == 'bluepin': self.renderer = sr_bluepin
					elif self.type == 'boot': self.renderer = sr_boot
					elif self.type == 'bow': self.renderer = sr_bow
				else:
					if self.type == 'arm': self.renderer = sr_arm
					elif self.type == 'conductor': self.renderer = sr_conductor
					elif self.type == 'chewedgum': self.renderer = sr_chewedgum
					elif self.type == 'dino': self.renderer = sr_dino
					elif self.type == 'dj': self.renderer = sr_dj
					elif self.type == 'enginenowheel': self.renderer = sr_enginenowheel
					elif self.type == 'enginewithwheel': self.renderer = sr_enginewithwheel
					elif self.type == 'gatedown': self.renderer = sr_gatedown
					elif self.type == 'gateup': self.renderer = sr_gateup
					elif self.type == 'getoutofjail': self.renderer = sr_getoutofjail
					elif self.type == 'guard': self.renderer = sr_guard
					elif self.type == 'goblet': self.renderer = sr_goblet
					elif self.type == 'hippochoke': self.renderer = sr_hippochoke
					elif self.type == 'hipposafe': self.renderer = sr_hipposafe
					elif self.type == 'horse': self.renderer = sr_horse
					elif self.type == 'joearm': self.renderer = sr_joearm
					elif self.type == 'joenoarm': self.renderer = sr_joenoarm
					elif self.type == 'joust': self.renderer = sr_joust
					elif self.type == 'king': self.renderer = sr_king
					elif self.type == 'knight1': self.renderer = sr_knight1
					elif self.type == 'knight2': self.renderer = sr_knight2
					elif self.type == 'legopog': self.renderer = sr_legopog
					elif self.type == 'mothercar1': self.renderer = sr_mothercar1
					elif self.type == 'mothercar2': self.renderer = sr_mothercar2
					elif self.type == 'passenger1sleeping': self.renderer = sr_passenger1sleeping
					elif self.type == 'passenger1awake': self.renderer = sr_passenger1awake
					elif self.type == 'passenger2': self.renderer = sr_passenger2
					elif self.type == 'photo4': self.renderer = sr_photo4
					elif self.type == 'queen': self.renderer = sr_queen
					elif self.type == 'racecar': self.renderer = sr_racecar
					elif self.type == 'raver1': self.renderer = sr_raver1
					elif self.type == 'raver2': self.renderer = sr_raver2
					elif self.type == 'rubberband': self.renderer = sr_rubberband
					elif self.type == 'rubberband2': self.renderer = sr_rubberband2
					elif self.type == 'scottie': self.renderer = sr_scottie
					elif self.type == 'steam': self.renderer = sr_steam
					elif self.type == 'teleporter': self.renderer = sr_teleporter
					elif self.type == 'teeth': self.renderer = sr_teeth
					elif self.type == 'thimble': self.renderer = sr_thimble
					elif self.type == 'tophat': self.renderer = sr_tophat
					elif self.type == 'traincar': self.renderer = sr_traincar
					elif self.type == 'trainpog': self.renderer = sr_trainpog
					elif self.type == 'trainwheel': self.renderer = sr_trainwheel
					elif self.type == 'ventalex': self.renderer = sr_ventalex
					elif self.type == 'volcanopog': self.renderer = sr_volcanopog
					elif self.type == 'wheelbarrow': self.renderer = sr_wheelbarrow
					elif self.type == 'wizard': self.renderer = sr_wizard
					
					elif self.type == 'house': self.renderer = sr_house
					
					elif self.type == 'legohack': self.renderer = sr_legohack
					elif self.type == 'horse1': self.renderer = sr_horse1
					elif self.type == 'horse2': self.renderer = sr_horse2
					elif self.type == 'horse2collapsed': self.renderer = sr_horse2collapsed
					elif self.type == 'spectator1': self.renderer = sr_spectator1
					elif self.type == 'spectator2': self.renderer = sr_spectator2
					elif self.type == 'sadman': self.renderer = sr_sadman
					elif self.type == 'trueking': self.renderer = sr_trueking
					elif self.type == 'cinematichack': self.renderer = sr_cinematichack
		
		#if self.renderer == None:
		#	$print(self.type)
		self.renderer(self, screen, images, rc)

def draw_image_centered(screen, sprite, img):
	w = $image_width(img)
	h = $image_height(img)
	x = sprite.x - $int(w / 2)
	y = sprite.y - h
	$image_blit(screen, img, x, y)
	sprite.last_width = w
	sprite.last_height = h
	#$print(sprite.type)

def draw_image_centered_directional(screen, sprite, images, key):
	img = images[key + '_' + sprite.last_direction]
	draw_image_centered(screen, sprite, img)


def sr_arm(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/misc/arm'])
def sr_ball(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/ball'])
def sr_battleship(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/battleship'])
def sr_bballplayer1(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/cards/red')
def sr_bballplayer2(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/cards/red')
def sr_bballplayer3(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/cards/red')
def sr_bluepin(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/bluepin'])
def sr_boot(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/boot'])
def sr_bow(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/bow'])
def sr_chewedgum(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/chewedgum'])
def sr_cinematichack(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['backgrounds/cinematichack'])
def sr_conductor(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/conductor'])
def sr_dj(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/dj'])
def sr_dino(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/dinos/trex')
def sr_enginenowheel(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/enginenowheel'])
def sr_enginewithwheel(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/enginewithwheel'])
def sr_gatedown(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/gatedown'])
def sr_gateup(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/gateup'])
def sr_getoutofjail(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/getoutofjail'])
def sr_guard(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/misc/guard'])
def sr_hippochoke(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/hippo/choking'])
def sr_hipposafe(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/hippo/hippo'])
def sr_horse(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/horse'])
def sr_house(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/house'])
def sr_joearm(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/misc/joe_arm'])
def sr_joenoarm(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/misc/joe_noarm'])
def sr_king(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/king'])
def sr_knight1(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/guard0'])
def sr_knight2(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/guard1'])
def sr_legopog(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/pog'])
def sr_passenger1sleeping(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/passenger1sleeping'])
def sr_passenger1awake(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/passenger1awake'])
def sr_passenger2(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/passenger2'])
def sr_photo4(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/photo4'])
def sr_queen(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/queen'])
def sr_raver1(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/raver1'])
def sr_raver2(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/raver2'])
def sr_racecar(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/racecar'])
def sr_rubberband(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/rubberband_ground'])
def sr_scottie(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/scottie'])
def sr_thimble(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/thimble'])
def sr_tophat(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/tophat'])
def sr_traincar(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/traincar'])
def sr_trainpog(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/trainpog'])
def sr_trainwheel(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/trains/trainwheel'])
def sr_volcanopog(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/volcanopog'])
def sr_ventalex(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['simple/ventalex'])
def sr_wheelbarrow(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['icons/wheelbarrow'])
def sr_wizard(sprite, screen, images, rc): draw_image_centered_directional(screen, sprite, images, 'sprites/cards/wizard')

# too lazy to alphabetize
def sr_legohack(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['backgrounds/legos1point5'])
def sr_horse1(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/horse0'])
def sr_horse2(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/horse1'])
def sr_horse2collapsed(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/horsecollapse'])
def sr_spectator1(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/spectator0'])
def sr_spectator2(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/spectator1'])
def sr_sadman(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/sadman'])
def sr_trueking(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/trueking'])
def sr_joust(sprite, screen, images, rc): draw_image_centered(screen, sprite, images['sprites/legos/joust'])

def sr_steam(sprite, screen, images, rc): 
	c = (sprite.x + rc) % 60
	if c < 30 and (c > 20 or c < 10):
		draw_image_centered(screen, sprite, images['simple/steam'])

def sr_rubberband2(sprite, screen, images, rc):
	if sprite.stretched:
		draw_image_centered(screen, sprite, images['sprites/misc4/rubber_stretched'])
	else:
		draw_image_centered(screen, sprite, images['sprites/misc4/rubber_unstretched'])

_sr_teeth_values = [0, 1, 2, 3, 2, 1, 0]
def sr_teeth(sprite, screen, images, rc): 
	if sprite.teething:
		index = $int(rc / 3)
		num = _sr_teeth_values[index % $list_length(_sr_teeth_values)]
		draw_image_centered(screen, sprite, images['sprites/teeth/teeth' + $str(num)])
	else:
		draw_image_centered(screen, sprite, images['sprites/teeth/teeth0'])

def sr_goblet(sprite, screen, images, rc):
	if sprite.log != None and sprite.log.get_int('HAS_BLUEPIN', 0) == 0:
		img = images['sprites/legos/goblet_pin']
	else:
		img = images['sprites/legos/goblet']
	draw_image_centered(screen, sprite, img)

def sr_mothercar1(sprite, screen, images, rc):
	key = 'sprites/mothercar/left1'
	if sprite.last_direction == 'e':
		key = 'sprites/mothercar/right1'
	draw_image_centered(screen, sprite, images[key])

def sr_mothercar2(sprite, screen, images, rc):
	key = 'sprites/mothercar/left2'
	if sprite.last_direction == 'e':
		key = 'sprites/mothercar/right2'
	draw_image_centered(screen, sprite, images[key])

def sr_player_double(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc_double/s0_alt'])

def sr_player_full(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc/s0_alt'])

def sr_player_half(sprite, screen, images, rc):
	draw_image_centered(screen, sprite, images['sprites/mc_half/s0_alt'])

def sr_teleporter(sprite, screen, images, rc):
	key = 'teleporter/frame' + $str($int(rc / 5) % 3 + 1)
	draw_image_centered(screen, sprite, images[key])
