def perform_touchy(walking_surface, area, region_id, game_log, x, y):
	area_id = area.id
	player = area.player
	pdx = player.x - x
	pdy = player.y - y
	d = (pdx ** 2 + pdy ** 2) ** .5
	fake_sprite = Sprite('ignore', x, y)
	# TODO: apply distance constraints to boxes
	if area_id == 'attic':
		if region_id == 'train_box':
			pt_attic_train_box(walking_surface, area, region_id, game_log)
		elif region_id == 'games_box':
			pt_attic_games_box(walking_surface, area, region_id, game_log)
		elif region_id == 'lego_box':
			pt_attic_legos_box(walking_surface, area, region_id, game_log)
		elif region_id == 'sports_box':
			pt_attic_sports_box(walking_surface, area, region_id, game_log)
		elif region_id == 'misc_box':
			pt_attic_misc_box(walking_surface, area, region_id, game_log)
	elif area_id == 'games2':
		if region_id == 'housepile':
			pt_games_take_house(walking_surface, area, game_log, fake_sprite, d)

def perform_touchy_sprite(walking_surface, area, sprite, game_log):
	type = sprite.type
	area_id = area.id
	player = area.player
	pdx = player.x - sprite.x
	pdy = player.y - sprite.y
	d = (pdx ** 2 + pdy ** 2) ** .5
	if area_id == 'games1':
		if type == 'ball':
			pt_games_take_ball(walking_surface, area, game_log, sprite, d)
		elif type == 'battleship':
			pt_games_take_battleship(walking_surface, area, game_log, sprite, d)
		elif type == 'hippochoke':
			pt_games_hippo_heimlich(walking_surface, area, game_log, sprite, d)
		elif type == 'racecar':
			pt_games_take_racecar(walking_surface, area, game_log, sprite, d)
	elif area_id == 'games2':
		if type == 'getoutofjail': pt_games_take_getoutofjail(walking_surface, area, game_log, sprite, d)
		elif type == 'photo4': pt_games_take_photo4(walking_surface, area, game_log, sprite, d)
	elif area_id == 'legos2':
		if type == 'bow': pt_misc_take_bow(walking_surface, area, game_log, sprite, d)
		elif type == 'legopog': pt_misc_take_legopog(walking_surface, area, game_log, sprite, d)
		elif type == 'joust': pt_take_joust(walking_surface, area, game_log, sprite, d)
	elif area_id == 'legos3':
		if type == 'goblet': pt_misc_take_bluepin(walking_surface, area, game_log, sprite, d)
		elif type == 'trainwheel': pt_misc_take_trainwheel(walking_surface, area, game_log, sprite, d)
		elif type == 'wheelbarrow': pt_misc_take_wheelbarrow(walking_surface, area, game_log, sprite, d)
	elif area_id == 'misc1':
		if type == 'boot': pt_misc_take_boot(walking_surface, area, game_log, sprite, d)
		elif type == 'thimble': pt_misc_take_thimble(walking_surface, area, game_log, sprite, d)
	elif area_id == 'misc4':
		if type == 'rubberband2': pt_misc_hurl_self(walking_surface, area, game_log, sprite, d)
		elif type == 'volcanopog': pt_take_volcanopog(walking_surface, area, game_log, sprite, d)
	elif area_id == 'sports1':
		if type == 'rubberband': pt_misc_take_rubberband(walking_surface, area, game_log, sprite, d)
	elif area_id == 'trains1':
		if type == 'tophat': pt_trains_take_tophat(walking_surface, area, game_log, sprite, d)
		elif type == 'enginewithwheel' or type == 'traincar':
			if game_log.get_int('TRAIN_RUNNING', 0) == 1:
				pt_trains_board_train(walking_surface, area, game_log)
	elif area_id == 'trains2':
		if type == 'scottie':
			pt_trains_take_scottie(walking_surface, area, game_log, sprite, d)
		elif type == 'enginewithwheel' or type == 'traincar':
			pt_trains_board_train(walking_surface, area, game_log)
	elif area_id == 'trains3':
		if type == 'trainpog': pt_take_trainpog(walking_surface, area, game_log, sprite, d)

def dist_check(walking_surface, sprite, area, required_distance):
	dx = sprite.x - area.player.x
	dy = sprite.y - area.player.y
	if dx ** 2 + dy ** 2 < required_distance ** 2:
		return True
	else:
		walking_surface.invoke_dialog(["You're not close enough."], None, None)
		return False


def pt_trains_board_train(walking_surface, area, game_log):
	for sprite in area.sprites:
		if sprite.type == 'enginewithwheel' or sprite.type == 'traincar' or sprite.type == 'scottie':
			pass
		else:
			sprite.x = 9999
	area.train_go = True

def pt_misc_give_glue(scene, area, log):
	log.set_int('HAS_GLUE', 2)
	arm = area.get_sprite_by_type('arm')
	joe = area.get_sprite_by_type('joenoarm')
	joearm = Sprite('joearm', joe.x, joe.y)
	$list_add(area.sprites, joearm)
	arm.dead = True
	joe.dead = True
	log.set_int('HAS_PHOTO1', 1)
	scene.invoke_dialog([
		"Wow, it's as good as new.",
		"Did you say you got this from",
		"the dinosaurs? Maybe it's time",
		"to end this silly war.",
		"Your country thanks you with",
		"this photo scrap."], None, None)
	

def pt_misc_hurl_self(scene, area, game_log, sprite, player_distance):
	if dist_check(scene, sprite, area, 60):
		scene.invoke_dialog([
			"Alex decides to hurl himself",
			"across using the rubber band."], None, None)
		$list_add(scene.timeouts, [3, pt_hurl_self1, [sprite]])
		$list_add(scene.timeouts, [20, pt_hurl_self2, [sprite]])
def pt_hurl_self1(scene, args):
	band = args[0]
	band.stretched = True
def pt_hurl_self2(scene, args):
	band = args[0]
	band.stretched = False
	old_v = scene.player.v
	scene.area.player.ghost = True
	scene.area.player.v = 8
	scene.area.player.waypoints = [(207, 58)]
	scene.area.player.enforce_waypoints = True
	$list_add(scene.timeouts, [23, pt_hurl_self3, [old_v]])
def pt_hurl_self3(scene, args):
	v = args[0]
	scene.area.player.ghost = False
	scene.area.player.v = v

def pt_take_joust_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_BAT', 1)
def pt_take_joust(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["Guess he won't be needing this,", "anymore."],
			pt_take_joust_doer, [sprite])
	
def pt_take_trainpog_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_TRAINPOG', 1)
def pt_take_trainpog(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["Alex takes the pog."],
			pt_take_trainpog_doer, [sprite])
	
def pt_take_photo4_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_PHOTO4', 1)
def pt_games_take_photo4(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["You found a photo piece!."],
			pt_take_photo4_doer, [sprite])

def pt_take_getoutofjail_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_GETOUTOFJAIL', 1)
def pt_games_take_getoutofjail(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["This seems rather useful."],
			pt_take_getoutofjail_doer, [sprite])

def pt_take_volcanopog_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_VOLCANOPOG', 1)
def pt_take_volcanopog(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["Alex takes the pog."],
			pt_take_volcanopog_doer, [sprite])

def pt_trains_take_scottie_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_SCOTTIE', 1)
def pt_trains_take_scottie(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["Alex always wanted a dog.", "Therefore he shall steal this one."],
			pt_trains_take_scottie_doer, [sprite])
	
def pt_misc_take_wheelbarrow_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_WHEELBARROW', 1)
def pt_misc_take_wheelbarrow(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["A wheelbarrow != wheel.", "Alex removes it from the pile."],
			pt_misc_take_wheelbarrow_doer, [sprite])
	
def pt_misc_take_trainwheel_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_TRAINWHEEL', 1)
def pt_misc_take_trainwheel(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		if game_log.get_int('TRAIN_FIXED', 0) == 0:
			walking_surface.invoke_dialog(["Why would you take the red wheel", "away from the rest of his friends?"], None, None)
		else:
			walking_surface.invoke_dialog(
				["Upon closer inspection, Alex", "realizes that the red wheel", "is actually for the train engine."],
				pt_misc_take_trainwheel_doer, [sprite])
	
def pt_games_take_house(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		if game_log.get_int('HAS_HOUSE', 0) == 0:
			walking_surface.invoke_dialog(
				["It's not every day you can find a",
				 "free house in this market. Alex",
				 "seizes the opportunity by grabbing",
				 "a house and puts it in his pocket."],
				None, None)
			game_log.set_int('HAS_HOUSE', 1)
		else:
			walking_surface.invoke_dialog(
				["You already have a house. If you",
				 "get any more houses you may have",
				 "to run for Congress which seems",
				 "more trouble than it's worth."],
				None, None)
			


def pt_trains_take_tophat_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_TOPHAT', 1)
def pt_trains_take_tophat(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 80):
		walking_surface.invoke_dialog(
			["Alex was always curious whether or",
			 "not he was capable of stealing a",
			 "hat from a sleeping person."],
			pt_trains_take_tophat_doer, [sprite])
	
def pt_games_take_battleship_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_BATTLESHIP', 1)
def pt_games_take_battleship(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["This doesn't belong with these.",
			 "It probably got confused."],
			pt_games_take_battleship_doer, [sprite])
	
def pt_games_take_ball_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_BALL', 1)
def pt_games_take_ball(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["Alex picks up the ball",
			 "covered in hippo spit and",
			 "puts it in his pocket."],
			pt_games_take_ball_doer, [sprite])

def pt_games_hippo_heimlich_post(walking_surface, args):
	walking_surface.invoke_dialog(
		["Wow, thanks for the Heimlich.",
		 "I don't know what I would",
		 "have done if you weren't around!",
		 "Guess I should chew my food",
		 "before trying to swallow it."], None, None)
def pt_games_hippo_heimlich(walking_surface, area, game_log, sprite, d):
	game_log.set_int('IS_HIPPO_SAFE', 1)
	ball = Sprite('ball', sprite.x, sprite.y - 12)
	$list_add(ball.waypoints, (138, 74))
	ball.v = 7
	$list_add(walking_surface.timeouts, [20, pt_games_hippo_heimlich_post, []])
	$list_add(area.sprites, ball)
	ns = Sprite('hipposafe', sprite.x, sprite.y)
	$list_add(area.sprites, ns)
	sprite.dead = True

def pt_games_take_racecar_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_RACECAR', 1)
def pt_games_take_racecar(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["Alex graciously takes the token."],
			pt_games_take_racecar_doer, [sprite])
			
def pt_misc_take_bow_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_BOW', 1)
def pt_misc_take_bow(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["With dinosaurs on the loose, one",
			 "can't be too careful."],
			pt_misc_take_bow_doer, [sprite])

def pt_misc_take_legopog_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_LEGOPOG', 1)
def pt_misc_take_legopog(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 40):
		walking_surface.invoke_dialog(
			["This doesn't belong here."],
			pt_misc_take_legopog_doer, [sprite])

def pt_misc_take_bluepin_doer(walking_surface, args):
	log = walking_surface.log
	if log.get_int('HAS_BLUEPIN', 0) == 0:
		log.set_int('HAS_BLUEPIN', 1)
def pt_misc_take_bluepin(walking_surface, area, game_log, sprite, player_distance):
	if game_log.get_int('HAS_BLUEPIN', 0) == 0:
		if dist_check(walking_surface, sprite, area, 40):
			walking_surface.invoke_dialog(
				["This doesn't belong here."],
				pt_misc_take_bluepin_doer, [sprite])

def pt_misc_take_rubberband_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_RUBBERBAND', 1)
def pt_misc_take_rubberband(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 50):
		walking_surface.invoke_dialog(
			["This could be useful."],
			pt_misc_take_rubberband_doer, [sprite])

def pt_misc_take_thimble_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_THIMBLE', 1)
def pt_misc_take_thimble(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 50):
		walking_surface.invoke_dialog(
			["Hmmm...this trashcan looks familiar."],
			pt_misc_take_thimble_doer, [sprite])

def pt_misc_take_boot_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_BOOT', 1)
def pt_misc_take_boot(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 50):
		walking_surface.invoke_dialog(
			["He won't miss this", "...probably"],
			pt_misc_take_boot_doer, [sprite])

def pt_attic_train_box_swapper(walking_surface, args): walking_surface.switch_area('trains1')
def pt_attic_train_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Alex is magically drawn", "into the trains box."],
		pt_attic_train_box_swapper, None)

def pt_attic_games_box_swapper(walking_surface, args): walking_surface.switch_area('games1')
def pt_attic_games_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Alex is magically drawn", "into the games box."],
		pt_attic_games_box_swapper, None)

def pt_attic_legos_box_swapper(walking_surface, args): walking_surface.switch_area('legos1')
def pt_attic_legos_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Alex is magically drawn", "into the Legos box."],
		pt_attic_legos_box_swapper, None)

def pt_attic_sports_box_swapper(walking_surface, args): walking_surface.switch_area('sports1')
def pt_attic_sports_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Alex is magically drawn", "into the sports box."],
		pt_attic_sports_box_swapper, None)

def pt_attic_misc_box_swapper(walking_surface, args): walking_surface.switch_area('misc1')
def pt_attic_misc_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Alex is magically drawn", "into the misc box."],
		pt_attic_misc_box_swapper, None)