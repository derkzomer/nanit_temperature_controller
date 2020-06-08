import requests,json,time,datetime,config

class temperature_controller(object):
	"""docstring for temperature_controller"""
	def __init__(self):
		self.token = config.token
		self.headers = {
			'Authorization': 'token f8f54d94e4456e02198bd90ce65b0a840886c6609cf9c69b',
			'nanit-api-version': '0',
			'X-Nanit-Service': '2.0.7.0',
			'X-Nanit-Platform': 'Android Google Pixel 2 XL',
			'User-agent': 'Dalvik/2.1.0 (Linux; U; Android 10; Pixel 2 XL Build/QQ2A.200501.001.B3)',
			'Host': 'api.nanit.com',
		}
		self.params = (
			('limit', '10'),
		)
		self.ts = int(round(time.time(),0))

	def connect(self):
		r = requests.get('https://api.nanit.com/babies/41b6360a/messages', headers=self.headers, params=self.params, verify=False)
		self.parse(r)
	
	def parse(self,r):

		temperatures = []
		timestamps = []

		events = json.loads(r.content)
		for event in events["messages"]:
			if event["type"] == "TEMPERATURE":
				temperatures.append(event)

		temperature = 0

		if len(temperatures) > 1:
			for ts in temperatures:
				timestamps.append(ts["time"])
			for t in temperatures: 
				if t["time"] == max(timestamps):
					temperature = t["data"]["value"]
		elif len(temperatures) == 1:
			temperature = temperatures[0]["data"]["value"]
		else:
			temperature = 99

		self.turn_on_heater(temperature)

	def turn_on_heater(self, temperature):

		url = "https://maker.ifttt.com/trigger/heater_on/with/key/dhUFZpVlHvfxzrOT332XlV"
		
		if temperature <= 19:

			d = datetime.datetime.utcfromtimestamp(3600 * ((self.ts + 1800) // 3600))
			
			if d.hour >= 9 and d.hour <= 20:
				print "Turning on heater"
				r = requests.get(url)
				self.log_heater_toggle()
			else:
				print "Outside of evening hours"
			

	def log_heater_toggle(self):
		f = open("./heater.log", "w")
		f.write(str(self.ts))
		f.close()

temperature_controller().connect()