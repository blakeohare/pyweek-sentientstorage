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
	if area_id == 'misc1':
		if type == 'boot': pt_misc_take_boot(walking_surface, area, game_log, sprite, d)

def dist_check(walking_surface, sprite, area, required_distance):
	dx = sprite.x - area.player.x
	dy = sprite.y - area.player.y
	if dx ** 2 + dy ** 2 < required_distance ** 2:
		return True
	else:
		walking_surface.invoke_dialog(["You're not close enough."], None, None)
		return False

def pt_misc_take_boot_doer(walking_surface, args):
	sprite = args[0]
	sprite.dead = True
	walking_surface.log.set_int('HAS_BOOT', 1)
def pt_misc_take_boot(walking_surface, area, game_log, sprite, player_distance):
	if dist_check(walking_surface, sprite, area, 30):
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