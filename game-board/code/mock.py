import time

class Mock(object):
	"""
	A mock player to demo the game.

	@param delay: An integer representing the seconds to wait before mock user action.
	"""

	def __init__(self, delay):
		self.delay = delay

	def state_0_to_1(self, src, dst, middle):
		time.sleep(self.delay)

		self.peer(src, middle)
		self.peer(middle, dst)

	def state_1_to_2(self, src, dst, middle):
		time.sleep(self.delay)

		self.peer(src, middle)
		self.peer(middle, dst)

	def state_2_to_3(self, all_nodes):
		time.sleep(self.delay)
		
		self.peer(all_nodes[0], all_nodes[1])
		self.peer(all_nodes[0], all_nodes[2])
		self.peer(all_nodes[10], all_nodes[7])
		self.peer(all_nodes[2], all_nodes[3])
		self.peer(all_nodes[3], all_nodes[5])
		self.peer(all_nodes[7], all_nodes[4])
		self.peer(all_nodes[6], all_nodes[2])
		self.peer(all_nodes[7], all_nodes[1])
		self.peer(all_nodes[0], all_nodes[4])
		self.peer(all_nodes[4], all_nodes[5])
		self.peer(all_nodes[2], all_nodes[4])
		self.peer(all_nodes[10], all_nodes[9])
		self.peer(all_nodes[3], all_nodes[9])
		self.peer(all_nodes[7], all_nodes[8])
		self.peer(all_nodes[6], all_nodes[8])
		self.peer(all_nodes[10], all_nodes[6])

	def peer(self, node0, node1):
		if node0 is not node1:
			node0.add_peer(node1)
			node1.add_peer(node0)
