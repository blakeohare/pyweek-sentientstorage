def perform_touchy(walking_surface, area, region_id, game_log):
	area_id = area.id
	if area_id == 'attic':
		if region_id == 'train_box':
			pt_attic_train_box(walking_surface, area, region_id, game_log)
	else:
		pass

def pt_attic_train_box_swapper(walking_surface):
	walking_surface.switch_area('trains1')

def pt_attic_train_box(walking_surface, area, region_id, game_log):
	# TODO: only show this once
	walking_surface.invoke_dialog(
		["Simon is magically drawn", "into the trains box."],
		pt_attic_train_box_swapper)
