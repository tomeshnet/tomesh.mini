import time

class Connectors(object):
	"""
	A set of connectors for a node.

	@param indicator: A GPIO for the LED indicator.
	@param towers: A list of GPIOs for towers.
	"""

	def __init__(self, indicator, towers):
		self.indicator = indicator
		self.towers = towers

	def indicator_on(self):
		self.indicator.high()

	def indicator_off(self):
		self.indicator.low()

	def indicator_flash(self, num_times):
		initial_high = self.indicator.is_high()
		while num_times > 0:
			self.indicator.high()
			time.sleep(1)
			self.indicator.low()
			time.sleep(1)
			num_times -= 1
		if initial_high:
			self.indicator.high()

	def detect_connection(self):
		for tower in self.towers:
			# print "Checking %s is_low=%s" % (tower.pin, tower.is_low())
			if tower.is_low():
				return tower
		return None
