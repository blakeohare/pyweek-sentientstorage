def apply_item(walky_surface, area, area_id, item, sprite, region_id):
	log = walky_surface.log
	if area_id == 'games1':
		if sprite != None:
			if sprite.type == 'mothercar1':
				if item == 'bluepin':
					ai_give_pin_to_mother(walky_surface, sprite, area, log)
	elif area_id == 'misc2':
		if sprite != None and sprite.type == 'guard':
			if item == 'bow':
				if log.get_int('GATE_OPEN', 0) == 0:
					ai_shooting_game(walky_surface, area, log)
	elif area_id == 'misc3':
		if sprite != None and sprite.type == 'teeth':
			if item == 'wrappedgum':
				ai_teeth_chew_gum(walky_surface, area, sprite, log)
		if item == 'chewedgum':
			walky_surface.invoke_dialog(["Alex throws the gum at the T-Rex"], ai_throw_gum, None)
	elif area_id == 'sports1':
		if sprite != None:
			if sprite.type == 'bballplayer1' or sprite.type == 'bballplayer2' or sprite.type == 'bballplayer3':
				if item == 'ball' or item == 'bat':
					has_both = log.get_int('HAS_BAT',0) == 2
					ai_give_ball_to_player(walky_surface, sprite, area, log, item, has_both)
				elif log.get_int('HAS_WRAPPEDGUM', 0) != 0:
					if item == 'house' or item == 'volcanopog' or item == 'legopog' or item == 'trainpog':
						ai_give_base_to_player(walky_surface, sprite, area, log, item)
	elif area_id == 'trains1':
		if sprite != None:
			if sprite.type == 'conductor' or sprite.type == 'enginenowheel':
				if item == 'trainwheel':
					ai_give_wheel_to_conductor(walky_surface, area, log)
	elif area_id == 'trains3':
		if item == 'wizard':
			ai_release_wizard(walky_surface, area, log)

def ai_throw_gum2(scene, args):
	scene.invoke_dialog([
		"It looks like he's stuck"], None, None)
def ai_throw_gum(scene, args):
	area = scene.area
	log = scene.log
	sprite = Sprite('chewedgum', area.player.x, area.player.y)
	sprite.v = 12.0
	$list_add(sprite.waypoints, [142, 84])
	dino = area.get_sprite_by_type('dino')
	$list_add(dino.waypoints, [142, 87])
	$list_add(scene.timeouts, [30 * 2, ai_throw_gum2, None])
	log.set_int('HAS_CHEWEDGUM', 2)
	log.set_int('DINO_STATE', 1)
	$list_add(area.sprites, sprite)

def ai_teeth_chew_gum2(scene, args):
	sprite = args[0]
	sprite.teething = False
	scene.invoke_dialog([
		"Alex's wrapped gum is now",
		"chewed gum and a wrapper."], None, None)
def ai_teeth_chew_gum(walky_surface, area, sprite, log):
	sprite.teething = True
	log.set_int('HAS_WRAPPEDGUM', 2)
	log.set_int('HAS_WRAPPER', 1)
	log.set_int('HAS_CHEWEDGUM', 1)
	$list_add(walky_surface.timeouts, [30 * 3, ai_teeth_chew_gum2, [sprite]])


def ai_shooting_game2(scene, args):
	scene.next = ShootingGame(scene)
	
def ai_shooting_game(walky_surface, area, log):
	walky_surface.invoke_dialog([
		"I see you have a bow and arrow.",
		"A bit unconventional, but I'll",
		"let it pass. As long as you can",
		"use it. Show me on that target",
		"over there."], ai_shooting_game2, [])

def ai_release_wizard(walky_surface, area, log):
	log.set_int('HAS_WIZARD', 2)
	$list_add(area.sprites, Sprite('wizard', 187, 132))
	walky_surface.invoke_dialog([
		"Now, THIS is my sort of scene.",
		"I bet they won't even be mad if",
		"I use my scepter effects."], None, None)
	

def ai_train_launch2(scene, args):
	scene.area.train_go = True
def ai_train_launch1(scene, args):
	scene.invoke_dialog([
		"Please put up all tray tables",
		"and keep all hands and feet in",
		"the bus at all times.",
		"And remember, the closest exit",
		"may be behind you.",
		"3...2...1...launch!"
		], None, None)
	$list_add(scene.timeouts, [20, ai_train_launch2, []])
	scene.player.x = 9999
	for sprite in scene.area.sprites:
		if sprite.type == 'enginewithwheel' or sprite.type == 'traincar':
			pass
		else:
			sprite.x = 9999
def ai_give_wheel_to_conductor(walky_surface, area, log):
	walky_surface.invoke_dialog([
			"Goodness, the missing wheel!",
			"Now we can set sail!"
			], None, None)
	log.set_int('HAS_TRAINWHEEL', 2)
	$list_add(walky_surface.timeouts, [20, ai_train_launch1, []])
	for sprite in area.sprites:
		if sprite.type == 'enginenowheel':
			sprite.dead = True
			$list_add(area.sprites, Sprite('enginewithwheel', sprite.x, sprite.y))
			return
	

def ai_give_ball_to_player(walky_surface, sprite, area, log, item, has_both):
	log.set_int('HAS_' + $string_upper(item), 2)
	if has_both:
		walky_surface.invoke_dialog([
				"Oh, look, a " + item + "!",
				"Now we can actually play some ball!",
				"Have some gum for your troubles."
				], None, None)
		log.set_int('HAS_WRAPPEDGUM', 1)
	else:
		if item == 'ball':
			walky_surface.invoke_dialog([
				"Oh, look, a ball!",
				"Now we just need a bat."], None, None)
		else:
			walky_surface.invoke_dialog([
				"Oh, look, a bat!",
				"Now we just need a ball."], None, None)
		
			

def ai_give_base_to_player(walky_surface, sprite, area, log, item):
	log.set_int('HAS_' + $string_upper(item), 2)
	
	sum = log.get_int('HAS_HOUSE', 0) + log.get_int('HAS_TRAINPOG', 0) + log.get_int('HAS_LEGOPOG', 0) + log.get_int('HAS_VOLCANOPOG', 0)
	if sum == 8:
		walky_surface.invoke_dialog([
			"Hey, we have all the bases now!",
			"Take this as a token of our ",
			"appreciation"
			], None, None)
	else:
		walk_surface.invoke_dialog([
			"Thanks! This will make seeing the",
			"bases easier.",
			"",
			"(He gives you a photo piece)"
		], None, None)
		

def ai_give_ball_and_bat_to_player(walky_surface, sprite, area, log):
	log.set_int('HAS_BALL', 2)
	log.set_int('HAS_BAT', 2)
	walky_surface.invoke_dialog([
		"Hooray!",
		"Now we can play.",
		"Have some buble gum for your troubles.",
		"Now if we only had some bases."], None, None)

def ai_give_pin_to_mother(walky_surface, sprite, area, log):
	sprite.dead = True
	ns = Sprite('mothercar2', sprite.x, sprite.y)
	ns.lifetime = sprite.lifetime
	$list_add(area.sprites, ns)
	walky_surface.invoke_dialog([
		"My baby!",
		"Where ever did you find him!",
		"Here, have a car token."], None, None)
	log.set_int('HAS_BLUEPIN', 2)
	log.set_int('SHOW_CAR_TOKEN', 1)
	$list_add(area.sprites, Sprite('racecar', ns.x, ns.y + 12))
	
	