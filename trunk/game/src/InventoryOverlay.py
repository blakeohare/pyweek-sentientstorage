ALL_ITEMS = [
		'bat',
		'ball',
		'battleship',
		'bluepin',
		'boot',
		'bow',
		'chewedgum',
		'getoutofjail',
		'glue',
		'house',
		'legopog',
		'racecar',
		'rubberband',
		'scottie',
		'thimble',
		'tophat',
		'trainpog',
		'trainwheel',
		'volcanopog',
		'wheelbarrow',
		'wizard',
		'wrappedgum',
		'wrapper',
		'photo1',
		'photo2',
		'photo3',
		'photo4',
		'photo5'
	]

ITEMS_PER_ROW = 5

class InventoryOverlay:
	def __init__(self, playscene):
		self.playscene = playscene
		self.next = self
		self.item_grid = self.build_item_grid(self.playscene.log)
		self.rectangles = None
			
	
	def build_item_grid(self, log):
		output = []
		index = 0
		for item in ALL_ITEMS:
			if log.get_int("HAS_" + $string_upper(item), 0) == 1:
				x = index % ITEMS_PER_ROW
				if x == 0:
					row = []
					for i in range(ITEMS_PER_ROW):
						$list_add(row, None)
					$list_add(output, row)
				y = $int(index / ITEMS_PER_ROW)
				output[y][x] = item
				index += 1
		self.has_any = index > 0
		return output
		
	def update(self, events):
		exit = False
		for ev in events:
			if ev.type == 'mouseleftdown':
				x = ev.x
				y = ev.y
				if self.rectangles != None:
					for rect in self.rectangles:
						if x > rect[0] and x < rect[2] and y > rect[1] and y < rect[3]:
							item = rect[4]
							self.playscene.cursor = CURSOR_ITEM
							self.playscene.active_item = item
							
				self.next = self.playscene
				self.playscene.next = self.playscene
				
			
	
	def render(self, screen, images, rc, is_primary):
		self.playscene.render(screen, images, rc, False)
		rectangles = []
		rowcount = $list_length(self.item_grid)
		
		width = ITEMS_PER_ROW * 32
		left = $int((320 - width) / 2)
		height = rowcount * 32
		top = $int((240 - height) / 2)
		$draw_rectangle(screen, left, top, width, height, 200, 200, 230)
		for y in range(rowcount):
			for x in range($list_length(self.item_grid[y])):
				item = self.item_grid[y][x]
				if item != None:
					rleft = x * 32 + left
					rtop = y * 32 + top
					$image_blit(screen, images['icons/' + item], rleft + 1, rtop + 1)
					if self.rectangles == None:
						$list_add(rectangles, (rleft, rtop, rleft + 32, rtop + 32, item))
		if self.rectangles == None:
			self.rectangles = rectangles
		if not self.has_any:
			$draw_rectangle(screen, 60, 80, 200, 50, 200, 200, 230)
			draw_text(screen, images, 80, 100, "You are not carrying anything.")
		if is_primary:
			render_cursor('pointy', None, screen, images)