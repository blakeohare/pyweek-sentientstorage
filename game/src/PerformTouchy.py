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

def pt_attic_train_box_swapper(walking_surface): walking_surface.switch_area('trains1')
def pt_attic_train_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Simon is magically drawn", "into the trains box."],
		pt_attic_train_box_swapper)

def pt_attic_games_box_swapper(walking_surface): walking_surface.switch_area('games1')
def pt_attic_games_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Simon is magically drawn", "into the games box."],
		pt_attic_games_box_swapper)

def pt_attic_legos_box_swapper(walking_surface): walking_surface.switch_area('legos1')
def pt_attic_legos_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Simon is magically drawn", "into the legos box."],
		pt_attic_legos_box_swapper)

def pt_attic_sports_box_swapper(walking_surface): walking_surface.switch_area('sports1')
def pt_attic_sports_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Simon is magically drawn", "into the sports box."],
		pt_attic_sports_box_swapper)

def pt_attic_misc_box_swapper(walking_surface): walking_surface.switch_area('misc1')
def pt_attic_misc_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Simon is magically drawn", "into the misc box."],
		pt_attic_misc_box_swapper)