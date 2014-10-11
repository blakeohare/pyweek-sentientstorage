def dinos_shpiel_1(scene):
	scene.log.set_int('HAS_GLUE', 1)
	scene.log.set_int('DINO_STATE', 2)
	scene.invoke_dialog([
		"Why, Alex, why have you done",
		"this to me?"], dinos_shpiel_2, None)
	
def dinos_shpiel_2(scene, args):
	scene.invoke_dialog([
		"I thought you were  going to bite",
		"my arm off like you did to the",
		"colonel!"], dinos_shpiel_3, None)

def dinos_shpiel_3(scene, args):
	scene.invoke_dialog([
		"Bite your arm? Heaven's no!",
		"I just wanted to share some",
		"socialist literature with you. And as",
		"for the colonel, I didn't bite his arm.",
		"He didn't keep his hand inside the",
		"train like he was supposed to."], dinos_shpiel_4, None)

def dinos_shpiel_4(scene, args):
	scene.invoke_dialog([
		"Wait, the colonel said you guys",
		"were Soviets."], dinos_shpiel_5, None)

def dinos_shpiel_5(scene, args):
	scene.invoke_dialog([
		"Balderdash. We're socialists. We",
		"believe in free thinking and free",
		"healthcare. Take this arm medicine",
		"to the colonel courtesy of the",
		"Dinosaur Public Health System."], dinos_shpiel_6, None)

def dinos_shpiel_6(scene, args):
	scene.invoke_dialog([
		"What about you and this gum?"], dinos_shpiel_7, None)

def dinos_shpiel_7(scene, args):
	scene.invoke_dialog([
		"Don't worry, we have a free",
		"public service to deal with things",
		"like this. They'll be here to free",
		"me in the next 4-12 weeks."], None, None)