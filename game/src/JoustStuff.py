def joust1b(scene, args):
	scene.invoke_dialog([
		"Death by what? Are you going to",
		"force me to step on you without",
		"any shoes or socks on?"], None, None)

def joust2b(scene, args):
	scene.invoke_dialog([
		"Isn't that redundant?"], joust2c, None)
def joust2c(scene, args):
	scene.invoke_dialog([
		"Alex is nervous as the horses",
		"begin to move."], None, None)
	horse1 = scene.area.get_sprite_by_type('horse1')
	horse2 = scene.area.get_sprite_by_type('horse2')
	horse1.v = 1
	horse2.v = 1
	horse1.waypoints = [(91, 130)]
	horse2.waypoints = [(204, 130)]
	
	$list_add(scene.timeouts, [30, joust2d, []])

def joust2d(scene, args):
	horse1 = scene.area.get_sprite_by_type('horse1')
	horse2 = scene.area.get_sprite_by_type('horse2')
	horse2.dead = True
	horse2collapsed = Sprite('horse2collapsed', horse2.x, horse2.y + 10)
	bat = Sprite('joust', horse2.x - 20, horse2.y)
	$list_add(scene.area.sprites, horse2collapsed)
	$list_add(scene.area.sprites, bat)
	horse1.waypoints = []
	$list_add(scene.timeouts, [20, joust2e, []])

def joust2e(scene, args):
	scene.invoke_dialog([
		"King: I declare Sir Alex the victor!"], joust2f, None)

def joust2f(scene, args):
	scene.invoke_dialog([
		"Alex thinks to himself how low the",
		"standards of jousting have fallen",
		"ever since the Edna incident."], None, None)
	scene.log.set_int("LEGO_STATE", 1)
	horse = scene.area.get_sprite_by_type('horse1')
	horse.dead = True
	player = scene.area.player
	player.x = horse.x
	player.y = horse.y