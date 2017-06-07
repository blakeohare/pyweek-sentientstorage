def render_cursor(type, item, screen, images):
	pos = get_mouse_position()
	x = pos[0]
	y = pos[1]
	
	if type == 'waity':
		$image_blit(screen, images['cursors/waity'], x, y)
	else:
		$image_blit(screen, images['cursors/pointy'], x, y)
		$image_blit(screen, images['cursors/' + type], x, y)
	
	if item != None:
		$image_blit(screen, images['icons/' + item], x, y)