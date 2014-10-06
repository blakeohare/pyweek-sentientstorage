class GameLog:
	def __init__(self):
		self.int_values = {}
		self.string_values = {}
	
	def get_int(self, key, default_value):
		return $dictionary_get_with_default(self.int_values, key, default_value)
	
	def set_int(self, key, value):
		self.int_values[key] = value
	
	def get_string(self, key, default_value):
		return $dictionary_get_with_default(self.string_values, key, default_value)
	
	def set_string(self, key, value):
		self.string_values[key] = value
	
	def serialize(self):
		output = []
		for key in $dictionary_keys(self.int_values):
			$list_add(output, 'i:' + key + ':' + $str(self.int_values[key]))
		for key in $dictionary_keys(self.string_values):
			value = self.string_values[key]
			if value == None:
				$list_add(output, 'n:' + key + ':@')
			else:
				$list_add(output, 's:' + key + ':' + self.string_values[key])
		
		return $list_join(output, "\n")
	
	def parse_from(self, data):
		self.int_values = {}
		self.string_values = {}
		for line in $string_split(data, '\n'):
			parts = $string_split(line, ':')
			type = $string_trim(parts[0])
			key = $string_trim(parts[1])
			value = parts[2]
			if type == 'i':
				self.int_values[key] = $parse_int(value)
			elif type == 'n':
				self.string_values[key] = None
			else:
				for i in range(3, $list_length(parts)):
					value += ':' + parts[i]
				value = $string_trim(value)
				self.string_values[key] = value
		