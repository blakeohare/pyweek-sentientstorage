def knights_shpiel_1(scene, args):
	scene.log.set_int('KNIGHTS_SHPIEL', 1)
	scene.invoke_dialog([
		"Knight 1: Halt! Who goes there?"], 
		knights_shpiel_2, [])

def knights_shpiel_2(scene, args):
	scene.invoke_dialog([
		"Umm...me. Alex. Can I come in?"], 
		knights_shpiel_3, [])
	
def knights_shpiel_3(scene, args):
	scene.invoke_dialog([
		"Knight 2: Nope. No one is getting",
		"in, by order of the King. And don't",
		"even try breaking down this wall.",
		"Our fortress is 100% impenetrable.",
		"Absolutely no way past this wall,",
		"no way in or out, nope nope."], 
		None, None)