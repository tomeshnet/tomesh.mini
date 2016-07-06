from path import Path

class Node(object):
	"""
	A single node in the network.

	@param name: A string representing the name of a node.
	@param peers: A list of directly connected nodes.
	@param connectors: A list of connectors for the node.
	@param online: A boolean representing whether the node is online.
	"""

	def __init__(self, name, peers, connectors, online=True):
		self.name = name
		self.peers = peers
		self.connectors = connectors
		self.online = online

	def reset_indicator(self):
		self.connectors.indicator_off()
		return self

	def reset_peers(self):
		self.peers = []
		return self

	def add_peer(self, node):
		self.peers.append(node)
		return self

	def find_paths(self, dst, search, paths):
		# Reject cyclic paths
		if self in search:
			return

		# Reject offline nodes
		if not self.online:
			return

		# End search if self is dst
		if self is dst:
			# Create path object
			path = Path()
			for hop in search:
				path.add_hop(hop)
			path.add_hop(self)
			
			# Add current search as path
			paths.append(path)
			return

		# Keep searching down peers
		for peer in self.peers:
			# Append self to current search
			new_search = list(search)
			new_search.append(self)

			# Recursive call to find paths on peer
			peer.find_paths(dst, new_search, paths)

	def has_path(self, dst):
		paths = []
		self.find_paths(dst, [], paths)
		return len(paths) > 0

	def take_offline(self):
		# Flash indicator
		self.connectors.indicator_flash(5)
		self.connectors.indicator_off()

		# Mark as offline
		self.online = False