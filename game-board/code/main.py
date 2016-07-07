# coding: utf-8
import sys
import time
from node import Node
from gpio import Gpio
from connectors import Connectors
from path import Path
from mock import Mock
from picontroller import PiController

############
# Constants
############

# The game will begin with linking up the first two nodes defined in this list
ALL_NODE_NAMES = [ "LITTLE ITALY", "CITY HALL", "ROM", "CASA LOMA", "JUNCTION", "CN TOWER", "KENSINGTON", "HIGH PARK", "LITTLE INDIA", "GREEK TOWN", "BEACHES" ]

# Special run modes
RUN_DIAGNOSTICS = False
MOCK_MODE = False
DEBUG_MODE = False

# Default game parameters
GAME_TOTAL_LINKS = 12
GAME_FIRST_LINK_0 = 10
GAME_FIRST_LINK_1 = 4
GAME_LED_FLASH_DELAY = 1
GAME_SCAN_DELAY = 1
GAME_STEP_DELAY = 5

# Diagnostic parameters
DIAG_PATH_SEARCH_SRC = 0
DIAG_PATH_SEARCH_DST = len(ALL_NODE_NAMES) - 1

# Mock parameters
MOCK_COUNTER = 1
MOCK_FIRST_LINK_MIDDLE_NODE = 2
MOCK_SECOND_LINK_MIDDLE_NODE = 3

# Connectors representing GPIO groupings
NODE_0 = Connectors(Gpio(Gpio.BUS_ADDR_0, Gpio.GPB0), [ Gpio(Gpio.BUS_ADDR_0, Gpio.GPB1), Gpio(Gpio.BUS_ADDR_0, Gpio.GPB2), Gpio(Gpio.BUS_ADDR_0, Gpio.GPB3), Gpio(Gpio.BUS_ADDR_0, Gpio.GPB4) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_1 = Connectors(Gpio(Gpio.BUS_ADDR_0, Gpio.GPB5), [ Gpio(Gpio.BUS_ADDR_0, Gpio.GPB6), Gpio(Gpio.BUS_ADDR_0, Gpio.GPA0), Gpio(Gpio.BUS_ADDR_0, Gpio.GPA1), Gpio(Gpio.BUS_ADDR_0, Gpio.GPA2) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_2 = Connectors(Gpio(Gpio.BUS_ADDR_0, Gpio.GPA7), [ Gpio(Gpio.BUS_ADDR_0, Gpio.GPA6), Gpio(Gpio.BUS_ADDR_0, Gpio.GPA5), Gpio(Gpio.BUS_ADDR_0, Gpio.GPA4), Gpio(Gpio.BUS_ADDR_0, Gpio.GPA3) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_3 = Connectors(Gpio(Gpio.BUS_ADDR_1, Gpio.GPB5), [ Gpio(Gpio.BUS_ADDR_1, Gpio.GPB6), Gpio(Gpio.BUS_ADDR_1, Gpio.GPB7), Gpio(Gpio.BUS_ADDR_1, Gpio.GPB4) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_4 = Connectors(Gpio(Gpio.BUS_ADDR_1, Gpio.GPB0), [ Gpio(Gpio.BUS_ADDR_1, Gpio.GPB1), Gpio(Gpio.BUS_ADDR_1, Gpio.GPB2), Gpio(Gpio.BUS_ADDR_1, Gpio.GPB3) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_5 = Connectors(Gpio(Gpio.BUS_ADDR_1, Gpio.GPA3), [ Gpio(Gpio.BUS_ADDR_1, Gpio.GPA2), Gpio(Gpio.BUS_ADDR_1, Gpio.GPA1), Gpio(Gpio.BUS_ADDR_1, Gpio.GPA0) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_6 = Connectors(Gpio(Gpio.BUS_ADDR_1, Gpio.GPA7), [ Gpio(Gpio.BUS_ADDR_1, Gpio.GPA6), Gpio(Gpio.BUS_ADDR_1, Gpio.GPA5), Gpio(Gpio.BUS_ADDR_1, Gpio.GPA4) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_7 = Connectors(Gpio(Gpio.BUS_ADDR_2, Gpio.GPB3), [ Gpio(Gpio.BUS_ADDR_2, Gpio.GPB0), Gpio(Gpio.BUS_ADDR_2, Gpio.GPB1), Gpio(Gpio.BUS_ADDR_2, Gpio.GPB2) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_8 = Connectors(Gpio(Gpio.BUS_ADDR_2, Gpio.GPB4), [ Gpio(Gpio.BUS_ADDR_2, Gpio.GPB5), Gpio(Gpio.BUS_ADDR_2, Gpio.GPB6), Gpio(Gpio.BUS_ADDR_2, Gpio.GPB7) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_9 = Connectors(Gpio(Gpio.BUS_ADDR_2, Gpio.GPA3), [ Gpio(Gpio.BUS_ADDR_2, Gpio.GPA2), Gpio(Gpio.BUS_ADDR_2, Gpio.GPA1), Gpio(Gpio.BUS_ADDR_2, Gpio.GPA0) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)
NODE_10 = Connectors(Gpio(Gpio.BUS_ADDR_2, Gpio.GPA7), [ Gpio(Gpio.BUS_ADDR_2, Gpio.GPA6), Gpio(Gpio.BUS_ADDR_2, Gpio.GPA5), Gpio(Gpio.BUS_ADDR_2, Gpio.GPA4) ], GAME_LED_FLASH_DELAY, DEBUG_MODE)

# Connectors mapping to each node
CONNECTORS_MAP = {
	"CN TOWER": NODE_0,
	"CITY HALL": NODE_1,
	"LITTLE ITALY": NODE_2,
	"ROM": NODE_3,
	"KENSINGTON": NODE_4,
	"HIGH PARK": NODE_5,
	"JUNCTION": NODE_6,
	"CASA LOMA": NODE_7,
	"LITTLE INDIA": NODE_8,
	"GREEK TOWN": NODE_9,
	"BEACHES": NODE_10
}

###################
# Global variables
###################

all_nodes = []
num_links = 0

#######
# Main
#######

def main(argv):
	# Initialize WiringPi
	PiController().setup()

	# Run diagnostics
	if RUN_DIAGNOSTICS:
		init()
		diag()

	# Play game
	init()
	play()

def init():
	global all_nodes
	global num_links

	all_nodes = []
	num_links = 0

	for name in ALL_NODE_NAMES:
		all_nodes.append(Node(name, [], CONNECTORS_MAP.get(name)))

def play():
	global all_nodes
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
		num_links = scan(GAME_SCAN_DELAY, DEBUG_MODE)

		# Check for conditions to transition to next state
		if node(GAME_FIRST_LINK_0).has_path(node(GAME_FIRST_LINK_1)):
			paths = []
			node(GAME_FIRST_LINK_0).find_paths(node(GAME_FIRST_LINK_1), [], paths)
			for path in paths:
				# Transition only if there is one single multi-hop path
				if len(paths) == 1 and path.num_hops() > 1:
					print "Communication established: %s" % path_as_string(path)

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
		num_links = scan(GAME_SCAN_DELAY, DEBUG_MODE)

		# Check for conditions to transition to next state
		if node(GAME_FIRST_LINK_0).has_path(node(GAME_FIRST_LINK_1)):
			paths = []
			node(GAME_FIRST_LINK_0).find_paths(node(GAME_FIRST_LINK_1), [], paths)
			for path in paths:
				print "Communication re-established: %s" % path_as_string(path)

			# Transition to next state of the game
			state = 2

		# Mock player if enabled
		if MOCK_MODE and player is not None:
			player.state_1_to_2(node(GAME_FIRST_LINK_0), node(GAME_FIRST_LINK_1), node(MOCK_SECOND_LINK_MIDDLE_NODE))

	# STATE 2: Build a redundant network to cover the entire city
	print "\nNow let's connect the entire city!"

	while state == 2:
		# Scan for paths
		if MOCK_MODE and player is not None:
			scan(GAME_SCAN_DELAY, DEBUG_MODE)
		else:
			num_links = scan(GAME_SCAN_DELAY, DEBUG_MODE)

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
				print "\033[91m" + "   _       "  + "\033[97m" + "                    _     " + "\033[00m"
				print "\033[91m" + "  | |_ ___ "  + "\033[97m" + " _ __ ___   ___ ___| |__  " + "\033[00m"
				print "\033[91m" + "  | __/ _ \\" + "\033[97m" + "| '_ ` _ \ / _ / __| '_ \ " + "\033[00m"
				print "\033[91m" + "  | || (_) "  + "\033[97m" + "| | | | | |  __\__ | | | |" + "\033[00m"
				print "\033[91m" + "   \__\___/"  + "\033[97m" + "|_| |_| |_|\___|___|_| |_|" + "\033[00m"

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

		# Find all the paths and sort by decreasing number of hops
		paths = []
		src.find_paths(dst, [], paths)
		sort_paths(paths)

		# Try to select a path to route
		if len(paths) > 0:
			# Route through the first path
			current_path = paths[0]
			path_string = path_as_string(current_path)

			# Print step
			if destroy:
				print "    %s is offline! Reconnecting through: %s" % (destroy.name, path_string)
			else:
				print "    Connecting through: %s" % path_string

			# Pick an intermediate node to destroy
			destroy = current_path.get_hop(current_path.num_hops() / 2)
		else:
			# Print destination unreachable
			print "    %s is offline! %s is no longer reachable :(" % (destroy.name, dst.name)
			break

	# Print game summary
	time.sleep(GAME_STEP_DELAY)
	offline_nodes = []
	for n in all_nodes:
		if not n.online:
			offline_nodes.append(n)

	print "\nYour network is able to maintain communication between %s and %s while %s nodes are offline!" % (src.name, dst.name, len(offline_nodes) - 1)

def diag():
	global all_nodes
	global num_links

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
	sort_paths(paths)
	for path in paths:
		print path_as_string(path)

def name(index):
	return ALL_NODE_NAMES[index]

def node(index):
	return all_nodes[index]

def scan(scan_delay, debug=False):
	time.sleep(scan_delay)

	# Reset state
	if debug:
		print ""

	for n in all_nodes:
		if debug:
			print "DEBUG Resetting state of %s" % n.name

		n.reset_indicator().reset_peers()

	if debug:
		print ""

	# Count number of links
	links_counter = 0

	# Scan all possible connections
	for n in all_nodes:
		if debug:
			print "DEBUG Scanning %s" % n.name
		for tower in n.connectors.towers:
			if debug:
				print "DEBUG   Pinging from Tower %s\n" % tower.pin
			tower.low()

			for detect in all_nodes:
				if detect != n and detect not in n.peers:
					if debug:
						print "DEBUG   Detecting ping at %s" % detect.name

					connected_tower = detect.connectors.detect_connection()
					if connected_tower:
						if debug:
							print "DEBUG     %s connected at Tower %s\n" % (detect.name, connected_tower.pin)

						peer(n, detect)
						links_counter += 1
					else:
						if debug:
							print "DEBUG     %s not connected\n" % detect.name
				else:
					if debug:
						print "DEBUG   Skipping %s\n" % detect.name
			
			# Put back to high state
			tower.high()

				if debug:
					time.sleep(1)

	if debug:
		print "DEBUG Scan completed with %s links" % links_counter

	return links_counter
	

def peer(node0, node1):
	if node0 is not node1:
		node0.add_peer(node1)
		node1.add_peer(node0)

def sort_paths(paths):
	for i in range(len(paths)):
		for j in range(len(paths) - 1, i, -1):
			if (paths[j].num_hops() > paths[j - 1].num_hops()):
				tmp = paths[j]
				paths[j] = paths[j - 1]
				paths[j - 1] = tmp

def print_node(node):
	print "Name: %s" % node.name
	print "Peers: %s" % node_name_array(node.peers)
	print "Online: %s" % node.online
	print "Towers: %s" % len(node.connectors.towers)
	print "----------------------------------------------------------------"

def node_name_array(nodes):
	name_array = []
	for node in nodes:
		name_array.append(node.name)
	return name_array

def path_as_string(path):
	node_names = node_name_array(path.hops)
	dst_name = node_names[len(node_names) - 1]

	path_string = ""
	for hop in node_names:
		path_string = path_string + "\033[92m" + hop + "\033[00m"
		if hop is not dst_name:
			 path_string = path_string + " ❯ "
	return path_string

if __name__ == "__main__":
	main(sys.argv)