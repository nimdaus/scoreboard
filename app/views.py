from app import app
from flask import Flask, jsonify, request, redirect, url_for, render_template, flash
import os
import json
from subprocess import check_call, Popen
import psutil
import socket
import time
import pytz # $ pip install pytz
from datetime import datetime
import sys
import platform

#python3  -m pip install backports.zoneinfo #if older python than 3.9

def load_status(): #load json with environment variables
	global active_status, active_version, uptime, active_time, load_avg, ip_address, hostname, cpu_thermal, kernel, operating_system, py_version

	script = 'main.py'
	active_status = 0
	active_version = 0

	for process in psutil.process_iter():
		if process.cmdline() == ['python', f'{script}']:
			active_status = "Running"
		else:
			active_status = "Not Detected"
	
	delta = datetime.now().replace(microsecond=0) - datetime.fromtimestamp(psutil.boot_time())
	uptime = str(delta)

	now = datetime.now()
	active_time = now.strftime("%b/%d/%Y %H:%M:%S")

	load_avg = psutil.getloadavg() #(0.18, 0.11, 0.1)

	netinfo = psutil.net_if_addrs() #wlan0 -- needs to be in config
	netip = str(network["wlan0"][0])
	ip = re.search('(\d+\.\d+\.\d+\.\d*)', netip)
	ip_address = ip.group(1)
	hostname = socket.gethostname()

	sensors = psutil.sensors_temperatures() #vcgencmd measure_temp #Also works
	thermal_temp = re.search(rf'{"current"}=(\d+\.\d*)', str(sensors["cpu_thermal"][0]))
	cpu_thermal = thermal_temp.group(1)

	kernel_cmd = subprocess.run(["uname", "-r"], capture_output=True, text=True)
	kernel = kernel_cmd.stdout

	operating_system_cmd = subprocess.run(["lsb_release", "-ds"], capture_output=True, text=True)
	operating_system = operating_system_cmd.stdout

	py_version = ".".join(map(str, sys.version_info[:3]))

	return active_status, active_version, uptime, active_time, load_avg, ip_address, hostname, cpu_thermal, kernel, operating_system, py_version

def load_config():
	global config, config_loaded, web_config, web_config_loaded
	config_loaded = False
	config = 0
	web_config_loaded = False
	web_config = 0
	if os.path.exists("~/scoreboard-webui/config/config.json"):
		with open("~/scoreboard-webui/config/config.json") as f:
			config = json.load(f)
		config_loaded = True
	return config, config_loaded
	if os.path.exists("~/scoreboard-webui/config/web_config.json"):
		with open("~/scoreboard-webui/config/web_config.json") as f:
			web_config = json.load(f)
		web_config_loaded = True
	return web_config, web_config_loaded

@app.route('/')
def status():
	load_status()
	load_config()
	return render_template("status.html", active_status=active_status, active_version=active_version, uptime=uptime, active_time=active_time, load_avg=load_avg, ip_address=ip_address, hostname=hostname, , cpu_thermal=cpu_thermal, kernel=kernel, operating_system=operating_system, py_version=py_version)

@app.route('/preferences', methods=["GET"])
def preferences():
	load_config()
	return render_template("preferences.html", config=config)

@app.route('/preferences', methods=["POST"])
def apply_preferences():
	req = request.form['timeFormat']
	print(req)
#	time_format = req.get("")
#	with open("/Users/jlambert/scoreboard-webui/config/config.json", "w") as f:
#		config["preferences"]["time_format"] = req["time_format"]
#		json.dump(config, f)
#		f.close()
#	return redirect(request.url)
	return redirect(url_for('preferences'))

#	if request.method == "GET":
#		if config_loaded is False:
#			flash("No Config!", "info")
#			return redirect(url_for("status"))
#		else:
#			team = request.form["team"]
#			return render_template("preferences.html", config=config)
#	else:
#		#update the json
#		req = request.get_json()
#		load_config()
#		return render_template("preferences.html", config=config)

'''
TEAMS SECTION
'''
@app.route('/teams')
def teams(): #Read-Only of all teams
	return render_template("teams.html", config=config)

@app.route('/nhl')
def nhl(): #R/W of NHL
	return render_template("nhl.html", config=config)

@app.route('/mlb')
def mlb(): #R/W of MLB
	return render_template("mlb.html", config=config)

@app.route('/nfl')
def nfl(): #R/W of NFL
	return render_template("nfl.html", config=config)

'''
BOARDS SECTION
'''
@app.route('/boards')
def boards():
	return render_template("boards.html", config=config)

@app.route('/scoreticker')
def scoreticker():
	return render_template("scoreticker.html", config=config)

@app.route('/seriesticker')
def seriesticker():
	return render_template("seriesticker.html", config=config)

@app.route('/standings')
def standings():
	return render_template("standings.html", config=config)

@app.route('/clock')
def clock():
	return render_template("clock.html", config=config)

@app.route('/covid19')
def convid19():
	return render_template("covid19.html", config=config)

@app.route('/weather')
def weather():
	return render_template("weather.html", config=config)

'''
STATES SECTION
'''
@app.route('/states')
def states():
	return render_template("teams.html", config=config)

@app.route('/off_day')
def off_day():
	return render_template("off_day.html", config=config)

@app.route('/scheduled')
def scheduled():
	return render_template("scheduled.html", config=config)

@app.route('/intermission')
def intermission():
	return render_template("intermission.html", config=config)

@app.route('/Post Game')
def post_game():
	return render_template("post_game.html", config=config)

'''
EXTRAS SECTION
'''
@app.route('/extras', methods=["GET", "PUT"])
def extras():
	if request.method == "GET":
		if config_loaded is False:
			flash("No Config!", "info")
			return redirect(url_for("status"))
		else:
			team = request.form["team"]
			return render_template("extras.html", data=config)
	else:
		#update the json
		load_config()
		return render_template("extras.html", data=config)

'''
UPGRADE SECTION
'''
@app.route('/upgrade', methods=["GET"])
def upgrade():
	#pull from git
	#install
	#re-start
	if process.cmdline() == ['python', 'main.py']:
		flash("Stopping Now!", "info")
		check_call(["pkill", "-9", "-f", main.py])
		return redirect(request.url)
	else:
		flash("Starting Now!", "info")
		#upgrade to subprocess command
		os.system("sudo python3 ~/nhl-led-scoreboard/src/main.py --led-gpio-mapping=adafruit-hat --led-brightness=60 --led-slowdown-gpio=2 --updatecheck=True")
		return redirect(request.url)

'''
POWER SECTION
'''
@app.route('/stopstart', methods=["GET"])
def stopstart():
	if process.cmdline() == ['python', 'main.py']:
		flash("Stopping Now!", "info")
		check_call(["pkill", "-9", "-f", main.py])
		return redirect(request.url)
	else:
		flash("Starting Now!", "info")
		#To be upgraded to subprocess command
		os.system("sudo python3 ~/nhl-led-scoreboard/src/main.py --led-gpio-mapping=adafruit-hat --led-brightness=60 --led-slowdown-gpio=2 --updatecheck=True")
		return redirect(request.url)

@app.route('/reload', methods=["GET"])
def reload():
	flash("Reloading Now!", "info")
	os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
	time.sleep(3)
	return redirect(request.url)

@app.route('/reset', methods=["GET"])
def reset():
	flash("Resetting Now!", "info")
	check_call(["pkill", "-9", "-f", main.py])
	#exit code 0 on success
	#upgrade to subprocess command
	os.system("sudo python3 ~/nhl-led-scoreboard/src/main.py --led-gpio-mapping=adafruit-hat --led-brightness=60 --led-slowdown-gpio=2 --updatecheck=True")
	time.sleep(3)
	return redirect(request.url)

@app.route('/restart', methods=["GET"])
def restart():
	flash("Restarting in 3 Seconds!", "info")
	os.system("shutdown /r /t 3")
	return redirect(request.url)