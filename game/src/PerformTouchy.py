def perform_touchy(walking_surface, area, region_id, game_log):
	area_id = area.id
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
	else:
		pass

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
		elif type == 'hippochoke':
			pt_games_hippo_heimlich(walking_surface, area, game_log, sprite, d)
		elif type == 'racecar':
			pt_games_take_racecar(walking_surface, area, game_log, sprite, d)
	elif area_id == 'legos2':
		if type == 'bow': pt_misc_take_bow(walking_surface, area, game_log, sprite, d)
		elif type == 'legopog': pt_misc_take_legopog(walking_surface, area, game_log, sprite, d)
	elif area_id == 'legos3':
		if type == 'bluepin': pt_misc_take_bluepin(walking_surface, area, game_log, sprite, d)
	elif area_id == 'misc1':
		if type == 'boot': pt_misc_take_boot(walking_surface, area, game_log, sprite, d)
		elif type == 'thimble': pt_misc_take_thimble(walking_surface, area, game_log, sprite, d)
	elif area_id == 'sports1':
		if type == 'rubberband': pt_misc_take_rubberband(walking_surface, area, game_log, sprite, d)

def dist_check(walking_surface, sprite, area, required_distance):
	dx = sprite.x - area.player.x
	dy = sprite.y - area.player.y
	if dx ** 2 + dy ** 2 < required_distance ** 2:
		return True
	else:
		walking_surface.invoke_dialog(["You're not close enough."], None, None)
		return False

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
			["Alex gracious takes the token."],
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
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_BLUEPIN', 1)
def pt_misc_take_bluepin(walking_surface, area, game_log, sprite, player_distance):
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