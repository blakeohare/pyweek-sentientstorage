def sprite_looky_talky(scene, sprite, is_looky):
	id = sprite.type
	is_talky = not is_looky
	log = scene.log
	
	if id == 'conductor':
		train_running = log.get_int('TRAIN_RUNNING', 0) == 1
		if is_looky:
			if train_running:
				return slt_invoke_basic(scene, ["A happy conductor drives the train."])
			else:
				return slt_invoke_basic(scene, ["The conductor looks really bored."])
		else:
			if not train_running:
				if log.get_int('TRAIN_FIXED', 0) == 1:
					return slt_invoke_basic(scene, [
						"Great! We have tracks!", 
						"But now we seem to be missing", 
						"a wheel."])
				else:
					log.set_int('TRAIN_ARRANGE_READY', 1)
					return slt_invoke_basic(scene, ["The tracks are a mess.", "If only I could transform into", "a giant and rearrange them", "myself"])
			else:
				return slt_invoke_basic(scene, ["All aboard!"])
	if id == 'guard':
		if is_talky:
			if log.get_int('GATE_OPEN', 0) == 1:
				return slt_invoke_basic(scene, ["Be careful."])
			else:
				return slt_invoke_basic(scene, ["Only armed soldiers are allowed", "beyond this point."])
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
	if id == 'wizard':
		if is_looky:
			return slt_invoke_basic(scene, [
				"A wizard awkwardly wanders",
				"amongst the baseball players,",
				"mumbling to himself."])
		else:
			if scene.log.get_int('SAW_NIGHTCLUB', 0) == 1:
				scene.invoke_dialog([
					"I think I'm done with this place...", 
					"What? There's a nightclub in Train", 
					"Town? Take me with you!"], wizard_joins_party, [sprite])
			else:
				slt_invoke_basic(scene, [
					"Everything here is sports sports", 
					"sports. No one seems to care that", 
					"the realm is under threat of dark", 
					"forces and there is a false king", 
					"on the throne of Legoville.", 
					"*sigh*"])
				
	return False

def slt_invoke_basic(walky_scene, text):
	walky_scene.invoke_dialog(text, None, None)
	return True


def wizard_joins_party(scene, args):
	sprite = args[0]
	sprite.dead = True
	scene.log.set_int('HAS_WIZARD', 1)
	scene.invoke_dialog(["A wizard has joined your party."], None, None)