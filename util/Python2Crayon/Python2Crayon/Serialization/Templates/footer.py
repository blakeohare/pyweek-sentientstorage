
_key_conversion = {
	pygame.K_SPACE: 'space',
	pygame.K_RETURN: 'enter',
	pygame.K_MINUS: '-',
	pygame.K_PLUS: '=',
	pygame.K_PERIOD: '.',
	pygame.K_COMMA: ',',
	
	pygame.K_RSHIFT: 'shift',
	pygame.K_LSHIFT: 'shift',
	pygame.K_RCTRL: 'ctrl',
	pygame.K_LCTRL: 'ctrl',
	pygame.K_RALT: 'alt',
	pygame.K_LALT: 'alt',
}
for i in range(0, 26):
	_key_conversion[pygame.K_a + i] = 'abcdefghijklmnopqrstuvwxyz'[i]
for i in range(0, 10):
	_key_conversion[pygame.K_0 + i] = str(i)
for i in range(0, 12):
	_key_conversion[pygame.K_F1 + i] = 'f' + str(i + 1)

_pseudo_file_system = %%%TEXT_FILES%%%

def read_file(file):
	return _pseudo_file_system[file]

_current_song = [None]
def play_music(song):
	if song == _current_song[0]:
		return

	if song == None:
		pygame.mixer.music.stop()
	else:
		_current_song[0] = song
		path = 'audio' + os.sep + 'music' + os.sep + song + '.ogg'
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(-1)

_current_mouse_position = [0, 0]

def get_mouse_position():
	return _current_mouse_position

def main():
	pygame.init()
	image_files = "%%%IMAGE_FILES%%%".split('|')
	image_library = {}
	images_root = %%%IMAGES_ROOT%%%
	for image_file in image_files:
		key = image_file.split('.')[0]
		path = image_file
		if len(images_root) != 0:
			path = images_root + '/' + path
		image_library[key] = pygame.image.load(path.replace('/', os.sep))
	rscreen = pygame.display.set_mode((%%%SCREEN_WIDTH%%%, %%%SCREEN_HEIGHT%%%))
	vscreen = pygame.Surface((%%%GAME_WIDTH%%%, %%%GAME_HEIGHT%%%))

	rwidth, rheight = rscreen.get_size()
	vwidth, vheight = vscreen.get_size()

	pygame.mouse.set_visible(False)

	active_scene = %%%START_SCENE%%%()

	clock = pygame.time.Clock()
	render_counter = 0

	while active_scene != None:
		events = []
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.MOUSEMOTION:
				p = event.pos
				x = p[0] * vwidth // rwidth
				y = p[1] * vheight // rheight
				_current_mouse_position[0] = x
				_current_mouse_position[1] = y
				events.append(Event('mousemove', None, x, y))
			elif event.type == pygame.QUIT:
				events.append(Event('quit', 'button', 0, 0))
			elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				key = _key_conversion.get(event.key)
				if key != None:
					if key == 'f4' and (keys[pygame.K_LALT] or keys[pygame.K_RALT]):
						events.append(Event('quit', 'alt-f4', 0, 0))
					else:
						events.append(Event('keydown' if event.type == pygame.KEYDOWN else 'keyup', key, 0, 0))
			elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
				p = event.pos
				key = 'mouse' + ('left' if event.button == 1 else 'right') + ('down' if event.type == pygame.MOUSEBUTTONDOWN else 'up')
				x = event.pos[0] * vwidth // rwidth
				y = event.pos[1] * vheight // rheight
				events.append(Event(key, None, x, y))

		active_scene.update(events)
		active_scene.render(vscreen, image_library, render_counter, True)
		active_scene = active_scene.next

		pygame.transform.scale(vscreen, rscreen.get_size(), rscreen)

		render_counter += 1

		pygame.display.flip()
		clock.tick(%%%FPS%%%)

main()
