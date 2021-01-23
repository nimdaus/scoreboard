# scoreboard

Flask based WebUI to Scoreboard App

Pull down:
git clone --recursive https://github.com/nimdaus/scoreboard
Virtual (one time):
python3 -m venv webui
activate virtual:
source webui/bin/activate
Install reqs (one time):
python3 -m pip install -r requirements.txt
set flask app:
export FLASK_APP=run.py
export FLASK_ENV=development
launch:
flask run
