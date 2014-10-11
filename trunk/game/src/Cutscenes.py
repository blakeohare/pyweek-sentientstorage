def cs_attic_intro1(scene):
	scene.invoke_dialog([
		"It's been a month since Dad",
		"passed, and you're finally",
		"clearing the house so it",
		"can be sold. You've gone",
		"through everything except the",
		"attic, where all your old toys",
		"are stored with the rest of",
		"the junk."], cs_attic_intro2, None)
def cs_attic_intro2(scene, args):
	scene.invoke_dialog([
		"You and Dad didn't really talk",
		"anymore, not after Mom passed,",
		"and you had hoped maybe going",
		"through the house you would",
		"find a photo of the three of you",
		"in happier times."], cs_attic_intro3, None)
def cs_attic_intro3(scene, args):
	scene.invoke_dialog([
		"But it seems like Dad got rid of",
		"them all. You seem to remember",
		"you had one, but one day you",
		"and Dad got into a fight and",
		"you ripped it up right in front",
		"of him."], cs_attic_intro4, None)
def cs_attic_intro4(scene, args):
	scene.invoke_dialog([
		"If it's still around it will be in",
		"scraps, but it's better than nothing.",
		"You slowly climb the stairs to the",
		"attic, hoping somehow you'll be",
		"able to find the photo, or at least",
		"what's left of it."], None, None)

def cs_attic_ending1(scene):
	scene.invoke_dialog([
		"You've finally found all the pieces", 
		"of the photo! Carefully you tape",
		"them back together, and the",
		"smiling faces of your parents",
		"give you a sense of peace."], cs_attic_ending2, None)

def cs_attic_ending2(scene, args):
	scene.invoke_dialog([
		"You regret not talking with your",
		"dad more, especially after Mom",
		"passed away, but somehow you",
		"feel like if he were here, he'd",
		"want you to know that everything",
		"was going to be alright."], cs_attic_ending3, None)

def cs_attic_ending3(scene, args):
	scene.invoke_dialog([
		"Taped photo in hand, you decide",
		"to head back downstairs so you",
		"can go out and buy a frame."], cs_attic_ending4, None)


def cs_attic_ending4(scene, args):
	scene.invoke_dialog([
		"Credits:",
		"Programming: Blake O'Hare",
		"Backgrounds: Angel McLaughlin",
		"Sprites: Christine Sandquist",
		"Music: Adrian Cline",
		"Writing: Laura Freer",
		"Maps: Brendan Nelson"], cs_attic_ending5, None)

def cs_attic_ending5(scene, args):
	scene.invoke_dialog([
		"Thank you for playing!"], cs_attic_ending6, None)

def cs_attic_ending6(scene, args):
	scene.log.set_int('RESET', 1)