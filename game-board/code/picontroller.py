# import wiringpi

class PiController(object):
	"""
	Abstraction for Raspberry Pi controller.
	"""

	def __init__(self):
		pass

	def setup(self):
		try:
			wiringpi.wiringPiSetup()
			wiringpi.mcp23017Setup(65, 0x20)
			wiringpi.mcp23017Setup(65 + 16, 0x21)
			wiringpi.mcp23017Setup(65 + 32, 0x22)
		except:
			pass

	def pin_mode(self, pin, mode):
		try:
			wiringpi.pinMode(pin, mode)
		except:
			pass

	def pull_up_dn_control(self, pin, mode):
		try:
			wiringpi.pullUpDnControl(pin, mode)
		except:
			pass
	
	def digital_write(self, pin, state):
		try:
			wiringpi.digitalWrite(pin, state)
		except:
			pass
	
	def digital_read(self, pin):
		try:
			return wiringpi.digitalRead(pin)
		except:
			return 0