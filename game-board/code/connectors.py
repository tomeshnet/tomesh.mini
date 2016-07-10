class Connectors(object):
	"""
	A set of connectors for a node.

	@param indicator: A GPIO for the LED indicator.
	@param towers: A list of GPIOs for towers.
	@param debug: A boolean to indicate whether in debug mode.
	"""

	def __init__(self, indicator, towers, debug=False):
		self.indicator = indicator
		self.towers = towers
		self.debug = debug

	def indicator_on(self):
		self.indicator.high()

	def indicator_off(self):
		self.indicator.low()

	def detect_connection(self):
		for tower in self.towers:
			if tower.is_low():
				if self.debug:
					print "DEBUG       Tower %s connected" % tower.pin
				return tower
			else:
				if self.debug:
					print "DEBUG       Tower %s not connected" % tower.pin
		return None