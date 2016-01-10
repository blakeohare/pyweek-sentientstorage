class ShootingGame:
	def __init__(self, bg):
		self.next = self
		self.bg = bg
		self.type = 'ShootingGame'
		self.pos = [320, 0]
		self.arrow = None
		self.tl = (24, 105)
		self.origin = (34, 142)
		self.slope = 0
		self.sprite_version = 1
		self.tries = 0
		self.target = (266, 119)
	
	def update(self):
		pos = get_mouse_position()
		x = pos[0]
		y = pos[1]
		dx = x - self.origin[0]
		dy = y - self.origin[1]
		if dx <= 0:
			dx = 1
		if dy > 0:
			dy = 0
		
		self.slope = -1.0 * dy / dx
		if self.slope > 10:
			self.sprite_version = 1
		elif self.slope > 3:
			self.sprite_version = 2
		elif self.slope > .75:
			self.sprite_version = 3
		elif self.slope > .2:
			self.sprite_version = 4
		else:
			self.sprite_version = 5
		
		
		if self.arrow != None:
			
			x = self.arrow[0]
			y = self.arrow[1]
			ox = x
			oy = y
			vx = self.arrow[2]
			vy = self.arrow[3]
			#$print($str(x) + ', ' + $str(y) + ', ' + $str(vx) + ', ' + $str(vy))
			vy += .4
			x += vx
			y += vy
			self.arrow[0] = x
			self.arrow[1] = y
			self.arrow[3] = vy
			self.arrow[4] = (ox, oy)
			if self.arrow[1] > 208:
				self.arrow = None
	
	def click_hand(self, x, y): self.click(x, y)
	def click_walk(self, x, y): self.click(x, y)
	def click_look(self, x, y): self.click(x, y)
	def click_talk(self, x, y): self.click(x, y)
	def click_item(self, x, y, item): self.click(x, y)
	
	def click(self, x, y):
		if self.arrow == None:
			self.tries += 1
			dx = 1
			dy = self.slope
			magnitude = (dy ** 2 + 1) ** .5
			velocity = 13
			dx = velocity * dx / magnitude
			dy = velocity * dy / magnitude
			self.arrow = [self.origin[0], self.origin[1], dx, -dy, None]
			
		
	
	def render_cursor(self, cursor_mode, active_item, screen, images):
		render_cursor('pointy', None, screen, images)
	
	def render(self, screen, images, rc):
		self.bg.render(screen, images, rc)
		$draw_rectangle(screen, 8, 8, 304, 192, 0, 0, 0)
		$image_blit(screen, images['backgrounds/shooting_bg'], 10, 10)
		$image_blit(screen, images['sprites/mc_shooting/shooting_base'], 24, 105)
		$image_blit(screen, images['sprites/mc_shooting/bow_' + $str(self.sprite_version)], 24, 105)
		if self.arrow != None:
			start_x = self.arrow[0]
			start_y = self.arrow[1]
			end_x = self.arrow[4][0]
			end_y = self.arrow[4][1]
			
			arrow_length = 15
			
			dx = end_x - start_x
			dy = end_y - start_y
			dist = (dx ** 2 + dy ** 2) ** .5
			if dist == 0:
				end_x = start_x - arrow_length
				end_y = start_y
			else:
				dx = arrow_length * dx / dist
				dy = arrow_length * dy / dist
				end_x = start_x + dx
				end_y = start_y + dy
			
				
			for i in range(10):
				p = i / 9.0
				ap = 1.0 - p
				x = start_x * p + end_x * ap
				y = start_y * p + end_y * ap
				$draw_rectangle(screen, $int(x), $int(y), 3, 3, 200, 128, 60)
				dx = x - self.target[0]
				dy = y - self.target[1]
				dist = (dx ** 2 + dy ** 2) ** .5
				if dist < 3:
					self.next = self.bg
					self.next.next = self.next
					tries = $str(self.tries)
					suffix = 'th'
					digits = $int(self.tries % 100)
					if digits == 11 or digits == 12 or digits == 13: suffix = 'th'
					else:
						digit = $int(self.tries % 10)
						if digit == 1: suffix = 'st'
						elif digit == 2: suffix = 'nd'
						elif digit == 3: suffix = 'rd'
						else: suffix = 'th'
						
					self.next.invoke_dialog([
						"Wow, that's some sharp shooting!",
						"You got that on just your " + tries + suffix,
						"try!",
						"Sure, I can open the gate for you"], open_the_gate, [])

def open_the_gate(scene, args):
	for sprite in scene.area.sprites:
		if sprite.type == 'gatedown':
			sprite.dead = True
	$list_add(scene.area.sprites, Sprite('gateup', 185, 90))
	scene.log.set_int('GATE_OPEN', 1)
	scene.area.remove_block_at(210, 89)
