def sprite_looky_talky(scene, sprite, is_looky):
	id = sprite.type
	is_talky = not is_looky
	
	if id == 'hippochoke':
		if is_looky:
			return slt_invoke_basic(scene, ["It looks like he's choking."])
		else:
			return slt_invoke_basic(scene, ["Gh....*HACK*...","...whheeez..", "kh...."])
	if id == 'mothercar1':
		if is_looky:
			return slt_invoke_basic(scene, ["A red car paces back and forth,", "worriedly."])
		else:
			return slt_invoke_basic(scene, ["Oh, my baby, my baby.", "I've lost my baby!"])
	if id == 'mothercar2':
		if is_looky:
			return slt_invoke_basic(scene, ["A red car paces back and forth,", "happily."])
		else:
			return slt_invoke_basic(scene, ["Oh, thank you!", "Thank you!", "Thank you!"])
	
	return False

def slt_invoke_basic(walky_scene, text):
	walky_scene.invoke_dialog(text, None, None)
	return True