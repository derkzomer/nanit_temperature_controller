import requests,time

class heater_controller(object):
	"""docstring for check_heater"""
	def __init__(self):
		self.f = open("./heater.log", "r")

	def check_time(self):
		last_toggle_ts = int(self.f.read())
		ts = int(round(time.time(),0))
		delta = ts - last_toggle_ts

		print delta

		if delta > 5:
			self.turn_off_heater()
		
	def turn_off_heater(self):

		url = "https://maker.ifttt.com/trigger/heater_off/with/key/dhUFZpVlHvfxzrOT332XlV"
		r = requests.get(url)

heater_controller().check_time()