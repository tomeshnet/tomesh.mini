from picontroller import PiController

class Gpio(object):
	"""
	The address of a GPIO pin.

	@param bus_address: A GPIO bus address.
	@param pin: A GPIO pin.
	"""

	# Bus addresses
	BUS_ADDR_0 = 0x20
	BUS_ADDR_1 = 0x21
	BUS_ADDR_2 = 0x22

	# Pins
	GPA0 = 65
	GPA1 = 66
	GPA2 = 67
	GPA3 = 68
	GPA4 = 69
	GPA5 = 70
	GPA6 = 71
	GPA7 = 72
	GPB0 = 73
	GPB1 = 74
	GPB2 = 75
	GPB3 = 76
	GPB4 = 77
	GPB5 = 78
	GPB6 = 79
	GPB7 = 80

	def __init__(self, bus_address, pin):
		self.bus_address = bus_address
		self.pin = pin + (bus_address - self.BUS_ADDR_0) * 16
		self.picontroller = PiController()

	def high(self):
		self.picontroller.pin_mode(self.pin, 1)
		self.picontroller.digital_write(self.pin, 1)

	def low(self):
		self.picontroller.pin_mode(self.pin, 1)
		self.picontroller.digital_write(self.pin, 0)

	def is_high(self):
		self.picontroller.pin_mode(self.pin, 0)
		self.picontroller.pull_up_dn_control(self.pin, 1)
		return self.picontroller.digital_read(self.pin) == 1

	def is_low(self):
		self.picontroller.pin_mode(self.pin, 0)
		self.picontroller.pull_up_dn_control(self.pin, 2)
		return self.picontroller.digital_read(self.pin) == 0