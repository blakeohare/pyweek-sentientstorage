def apply_item(walky_surface, area, area_id, item, sprite, region_id):
	log = walky_surface.log
	if area_id == 'games1':
		if sprite != None:
			if sprite.type == 'mothercar1':
				if item == 'bluepin':
					ai_give_pin_to_mother(walky_surface, sprite, area, log)
	elif area_id == 'games2':
		if region_id != None and region_id != 'housepile':
			found = False
			for token in ALL_TOKEN_KEYS:
				if token == item:
					found = True
					break
			if found:
				slot_key = $string_upper(region_id) + "_TAKEN"
				if log.get_int(slot_key, 0) == 0:
					log.set_int(slot_key, 1)
					log.set_int('HAS_' + $string_upper(item), 2)
					i = $parse_int(slot_key[4]) - 1
					log.set_int($string_upper(item) + '_INDEX', i)
					coord = MONOPOLY_INDEX[i]
					sprite = Sprite(item, coord[0], coord[1])
					$list_add(area.sprites, sprite)
		
		if log.get_int('HAS_PHOTO4', 0) == 0:
			total = 0
			for i in range(1, 9):
				if log.get_int("SLOT" + $str(i) + "_TAKEN", 0) == 1:
					total += 1
			if total == 8:
				log.set_int("SHOW_PHOTO4", 1)
				log.set_int("SHOW_GETOUTOFJAIL", 1)
				s1 = Sprite('photo4', 160, 0)
				s2 = Sprite('getoutofjail', 160, 0)
				s1.ghost = True
				s2.ghost = True
				w1 = [(160, 0)]
				w2 = [(160, 0)]
				for i in range(40):
					x = $math_sin(i * 3.14159 * 2 / 20) * 80 * i / 40
					$list_add(w1, (-x + 160, i * 2))
					$list_add(w2, (x + 160, i * 2))
				s1.waypoints = w1
				s2.waypoints = w2
				$list_add(area.sprites, s1)
				$list_add(area.sprites, s2)
	elif area_id == 'legos2':
		if item == 'getoutofjail':
			pos = get_mouse_position()
			x = pos[0]
			y = pos[1]
			if x > 251 and y < 85 and y > 50:
				ai_free_king(walky_surface)
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
	elif area_id == 'misc4':
		if region_id == 'band' and item == 'rubberband':
			ai_rubberband_stretch(walky_surface, area, log)
		if region_id == 'vents' and item == 'wrapper':
			ai_vent_parachute(walky_surface, area, log)
		if sprite != None and sprite.type == 'steam' and item == 'wrapper':
			ai_vent_parachute(walky_surface, area, log)
	elif area_id == 'sports1':
		if sprite != None:
			if sprite.type == 'bballplayer1' or sprite.type == 'bballplayer2' or sprite.type == 'bballplayer3':
				if item == 'ball':
					has_both = log.get_int('HAS_BAT', 0)
					ai_give_ball_to_player(walky_surface, sprite, area, log, item, has_both)
				elif item == 'bat':
					has_both = log.get_int('HAS_BALL', 0) == 2
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

def ai_free_king(scene):
	if scene.log.get_int("LEGO_STATE", 0) == 2:
		return
	scene.log.set_int('LEGO_STATE', 2)
	scene.log.set_int('HAS_GETOUTOFJAIL', 2)
	area = scene.area
	sadman = area.get_sprite_by_type('sadman')
	sadman.dead = True
	trueking = Sprite('trueking', 300, 98)
	$list_add(area.sprites, trueking)
	scene.invoke_dialog(["As if by magic, the police", "car door opens."], ai_free_king2, None)
def ai_free_king2(scene, args):
	scene.invoke_dialog([
		"Gasp! It's the true king of",
		"Legoville!"], ai_free_king3, None)
def ai_free_king3(scene, args):
	scene.invoke_dialog([
		"True King: And I challenge you,",
		"false king, to an epic cinematic",
		"duel to death!"], ai_free_king4, None)
def ai_free_king4(scene, args):
	scene.invoke_dialog([
		"False King: I accept!"], ai_free_king5, None)
def ai_free_king5(scene, args):
	sprite = Sprite('cinematichack', 160, 208)
	falseking = scene.area.get_sprite_by_type('king')
	trueking = scene.area.get_sprite_by_type('trueking')
	trueking.x = falseking.x
	trueking.y = falseking.y
	falseking.dead = True
	$list_add(scene.area.sprites, sprite)
	$list_add(scene.timeouts, [120, ai_free_king6a, []])
def ai_free_king6a(scene, args):
	scene.area.get_sprite_by_type('cinematichack').dead = True
	$list_add(scene.timeouts, [10, ai_free_king6b, []])
def ai_free_king6b(scene, args):
	$list_add(scene.timeouts, [1, ai_free_king7, []])
def ai_free_king7(scene, args):
	scene.invoke_dialog([
		"Long live the new king!"], ai_free_king8, None)
def ai_free_king8(scene, args):
	scene.invoke_dialog([
		"True King: Our kingdom is in",
		"your debt, Sir Alex. Please",
		"take this photo scrap as a",
		"token of our appreciation."], None, None)
	scene.log.set_int('HAS_PHOTO5', 1)
	

def ai_vent_parachute(scene, area, log):
	dx = area.player.x - 155
	dy = area.player.y - 47
	dist = (dx ** 2 + dy ** 2) ** .5
	if dist > 40:
		scene.invoke_dialog([
			"You're too far away."], None, None)
	else:
		scene.invoke_dialog([
			"Using the gum wrapper as a glider,",
			"Alex parachutes down to the lower",
			"ledge using the steam vents as a",
			"boost."], None, None)
		proxy = Sprite('ventalex', scene.area.player.x, scene.area.player.y)
		scene.area.player.x = 999999
		proxy.ghost = True
		proxy.waypoints = [(85, 163)]
		$list_add(area.sprites, proxy)
		$list_add(scene.timeouts, [30 * 4, ai_vent_parachute2, [proxy]])
def ai_vent_parachute2(scene, args):
	proxy = args[0]
	proxy.dead = True
	scene.area.player.x = 85
	scene.area.player.y = 163

def ai_rubberband_stretch(scene, area, log):
	scene.invoke_dialog([
		"Alex stretches the rubber band",
		"between two stalagmites."], None, None)
	log.set_int('HAS_RUBBERBAND', 2)
	sprite = Sprite('rubberband2', 70, 201)
	$list_add(area.sprites, sprite)

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
	log.set_int('TRAIN_RUNNING', 1)
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
	if item == 'legopog':
		sprite = Sprite('legopog', 147, 159)
	elif item == 'volcanopog':
		sprite = Sprite(item, 253, 160)
	elif item == 'trainpog':
		sprite = Sprite(item, 239, 100)
	else:
		sprite = Sprite(item, 147, 96)
	$list_add(area.sprites, sprite)
	
	if sum == 8:
		walky_surface.invoke_dialog([
			"Hey, we have all the bases now!",
			"Take this as a token of our ",
			"appreciation",
			"",
			"(He gives you a photo piece)"
			], None, None)
		log.set_int('HAS_PHOTO2', 1)
	else:
		walky_surface.invoke_dialog([
			"Thanks! This will make seeing the",
			"bases easier."
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
	
	