def apply_item(walky_surface, area, area_id, item, sprite, region_id):
	log = walky_surface.log
	if area_id == 'games1':
		if sprite != None:
			if sprite.type == 'mothercar1':
				if item == 'bluepin':
					ai_give_pin_to_mother(walky_surface, sprite, area, log)

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
	
	