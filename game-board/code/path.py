class Path(object):
	"""
	A path between two nodes in the network.
	"""

	def __init__(self):
		self.hops = []

	def num_hops(self):
		return len(self.hops) - 1

	def add_hop(self, node):
		self.hops.append(node)
		return self

	def get_hop(self, hop_num):
		if hop_num <= self.num_hops():
			return self.hops[hop_num]
		return None

	def flash(self):
		for hop in self.hops:
			hop.connectors.indicator_on()
