import sys
import time
from node import Node
from path import Path
from mock import Mock

############
# Constants
############

# The game will begin with linking up the first two nodes defined in this list
ALL_NODE_NAMES = [ "LITTLE ITALY", "CITY HALL", "ROM", "CASA LOMA", "JUNCTION", "CN TOWER", "KENSINGTON", "HIGH PARK", "LITTLE INDIA", "GREEK TOWN", "BEACHES" ]

# Special run modes
RUN_DIAGNOSTICS = False
MOCK_MODE = True

# Default game parameters
GAME_TOTAL_LINKS = 16
GAME_FIRST_LINK_0 = 0
GAME_FIRST_LINK_1 = 1
GAME_STEP_DELAY = 10

# Diagnostic parameters
DIAG_PATH_SEARCH_SRC = 0
DIAG_PATH_SEARCH_DST = len(ALL_NODE_NAMES) - 1

# Mock parameters
MOCK_COUNTER = 5
MOCK_FIRST_LINK_MIDDLE_NODE = 2
MOCK_SECOND_LINK_MIDDLE_NODE = 3

###################
# Global variables
###################

all_nodes = []
num_links = 0

#######
# Main
#######

def main(argv):
	init()
	
	# Run diagnostics
	if RUN_DIAGNOSTICS:
		diag()

	# Play game
	play()

def init():
	for name in ALL_NODE_NAMES:
		all_nodes.append(Node(name, []))

def play():
	global num_links

	# Mock player if enabled
	player = None
	if MOCK_MODE:
		player = Mock(MOCK_COUNTER)

	# STATE 0: Create a multi-hop path between GAME_FIRST_LINK_0 and GAME_FIRST_LINK_1
	state = 0
	print "\nLink up %s with %s ..." % (name(GAME_FIRST_LINK_0), name(GAME_FIRST_LINK_1))

	while state == 0:
		# Scan for paths
		scan()

		# Check for conditions to transition to next state
		if node(GAME_FIRST_LINK_0).has_path(node(GAME_FIRST_LINK_1)):
			paths = []
			node(GAME_FIRST_LINK_0).find_paths(node(GAME_FIRST_LINK_1), [], paths)
			for path in paths:
				# Transition only if there is one single multi-hop path
				if len(paths) == 1 and path.num_hops() > 1:
					print "Communication established: %s" % node_name_array(path.hops)

					# Remember a middle node critical for routing
					critical = path.get_hop(1)

					# Transition to next state of the game
					state = 1

		# Mock player if enabled
		if MOCK_MODE and player is not None:
			player.state_0_to_1(node(GAME_FIRST_LINK_0), node(GAME_FIRST_LINK_1), node(MOCK_FIRST_LINK_MIDDLE_NODE))

	# STATE 1: Build alternative link between GAME_FIRST_LINK_0 and GAME_FIRST_LINK_1
	print "\nOh no! %s just went down. Is there an alternative path between %s and %s?" % (critical.name, name(GAME_FIRST_LINK_0), name(GAME_FIRST_LINK_1))

	# Take critical node offline
	critical.take_offline()

	while state == 1:
		# Scan for paths
		scan()

		# Check for conditions to transition to next state
		if node(GAME_FIRST_LINK_0).has_path(node(GAME_FIRST_LINK_1)):
			paths = []
			node(GAME_FIRST_LINK_0).find_paths(node(GAME_FIRST_LINK_1), [], paths)
			for path in paths:
				print "Communication re-established: %s" % node_name_array(path.hops)

			# Transition to next state of the game
			state = 2

		# Mock player if enabled
		if MOCK_MODE and player is not None:
			player.state_1_to_2(node(GAME_FIRST_LINK_0), node(GAME_FIRST_LINK_1), node(MOCK_SECOND_LINK_MIDDLE_NODE))

	# STATE 2: Build a redundant network to cover the entire city
	print "\nNow let's connect the entire city!"

	while state == 2:
		# Scan for paths
		scan()

		# Check that available links are all used up
		if num_links == GAME_TOTAL_LINKS:
			# Check that every node is connected to the network
			all_connected = True
			for n in all_nodes:
				if len(n.peers) == 0:
					all_connected = False
			
			if all_connected:
				print "Looks like you have just built the Toronto Mesh :)"
				print ""
				print "   _                           _     "
				print "  | |_ ___  _ __ ___   ___ ___| |__  "
				print "  | __/ _ \| '_ ` _ \ / _ / __| '_ \ "
				print "  | || (_) | | | | | |  __\__ | | | |"
				print "   \__\___/|_| |_| |_|\___|___|_| |_|"

				# Transition to next state of the game
				state = 3

		# Mock player if enabled
		if MOCK_MODE and player is not None:
			player.state_2_to_3(all_nodes)
			num_links = GAME_TOTAL_LINKS

	time.sleep(GAME_STEP_DELAY)

	# STATE 3: Check how well the mesh network holds up to failing nodes
	src = node(0)
	dst = None

	# Pick source node as an online node with most number of immediate peers
	for n in all_nodes:
		if n.online and n.peers >= src.peers:
			src = n

	# Pick destination node as an online non-peer node that has the most number of paths to source
	max_num_paths = 0
	for n in all_nodes:
		if n.online and src not in n.peers:
			paths = []
			n.find_paths(src, [], paths)
			num_paths = len(paths)
			if num_paths > max_num_paths:
				dst = n
				max_num_paths = num_paths

	# Start the scoring steps
	print "\nLet's see how well it holds up. %s calling %s ..." % (src.name, dst.name)

	# Start taking intermediate nodes offline one by one
	destroy = None
	while True:
		# Destroy a node if destroy is set
		if destroy:
			destroy.take_offline()
			time.sleep(GAME_STEP_DELAY)

		# Find all the paths
		paths = []
		src.find_paths(dst, [], paths)
		# TODO Sort paths list by decreasing number of hops

		# Try to select a path to route
		if len(paths) > 0:
			# Route through the first path
			current_path = paths[0]
			path_string = ""
			for hop in node_name_array(current_path.hops):
				path_string = path_string + hop
				if hop is not dst.name:
					 path_string = path_string + " -> "

			# Print step
			if destroy:
				print "    %s is offline! Reconnecting through: %s" % (destroy.name, path_string)
			else:
				print "    Connecting through: %s" % path_string

			# Pick an intermediate node to destroy
			destroy = current_path.get_hop(current_path.num_hops() / 2)
		else:
			# Print destination unreachable
			print "    %s is destroyed! %s is no longer reachable :(" % (destroy.name, dst.name)
			break

	# Print game summary
	time.sleep(GAME_STEP_DELAY)
	offline_nodes = []
	for n in all_nodes:
		if not n.online:
			offline_nodes.append(n)

	print "\nYour network is able to maintain communication between %s and %s while %s nodes are offline!" % (src.name, dst.name, len(offline_nodes))

def diag():
	# Set up test links
	peer(node(0), node(1))
	peer(node(0), node(2))
	peer(node(10), node(7))
	peer(node(2), node(3))
	peer(node(3), node(5))
	peer(node(7), node(4))
	peer(node(6), node(2))
	peer(node(7), node(1))
	peer(node(0), node(4))
	peer(node(4), node(5))
	peer(node(2), node(4))
	peer(node(10), node(9))
	peer(node(3), node(9))
	peer(node(7), node(8))
	peer(node(6), node(8))
	peer(node(10), node(6))

	# Print all nodes
	print "Nodes"
	print "================================================================"
	for n in all_nodes:
		print_node(n)

	# Print path search results
	print "Paths from %s to %s" % (name(DIAG_PATH_SEARCH_SRC), name(DIAG_PATH_SEARCH_DST))
	print "================================================================"
	paths = []
	node(DIAG_PATH_SEARCH_SRC).find_paths(node(DIAG_PATH_SEARCH_DST), [], paths)
	for path in paths:
		print node_name_array(path.hops)

def name(index):
	return ALL_NODE_NAMES[index]

def node(index):
	return all_nodes[index]

def scan():
	time.sleep(1)

	# TODO Scan all possible connections and update num_links

def peer(node0, node1):
	if node0 is not node1:
		node0.add_peer(node1)
		node1.add_peer(node0)

def print_node(node):
	print "Name: %s" % node.name
	print "Peers: %s" % node_name_array(node.peers)
	print "Indicator: %s" % node.indicator
	print "----------------------------------------------------------------"

def node_name_array(nodes):
	name_array = []
	for node in nodes:
		name_array.append(node.name)
	return name_array

if __name__ == "__main__":
	main(sys.argv)