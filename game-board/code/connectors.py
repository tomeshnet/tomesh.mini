import time

class Connectors(object):
	"""
	A set of connectors for a node.

	@param indicator: A GPIO for the LED indicator.
	@param towers: A list of GPIOs for towers.
	@param flash_delay: An integer representing the seconds between on/off state of a flashing indicator.
	@param debug: A boolean to indicate whether in debug mode.
	"""

	def __init__(self, indicator, towers, flash_delay, debug=False):
		self.indicator = indicator
		self.towers = towers
		self.flash_delay = flash_delay
		self.debug = debug

	def indicator_on(self):
		self.indicator.high()

	def indicator_off(self):
		self.indicator.low()

	def indicator_flash(self, num_times):
		initial_high = self.indicator.is_high()
		while num_times > 0:
			self.indicator.high()
			time.sleep(self.flash_delay)
			self.indicator.low()
			time.sleep(self.flash_delay)
			num_times -= 1
		if initial_high:
			self.indicator.high()

	def detect_connection(self):
		for tower in self.towers:
			if tower.is_high():
				if self.debug:
					print "DEBUG       Tower %s connected" % tower.pin
				return tower
			else:
				if self.debug:
					print "DEBUG       Tower %s not connected" % tower.pin
		return None