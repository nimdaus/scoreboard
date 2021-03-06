import subprocess
from subprocess import check_call, Popen
import time

print("Killing WebUI")
try:
	check_call(["pkill", "-9", "-f", "flask"])
except Exception:
	pass

print("Refreshing from source and restarting")
try:
	check_call(["pkill", "-9", "-f", "webui"])
except Exception:
	pass

subprocess.call()

proc = subprocess.Popen('screen -S webui', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
proc.stdin.write(git reset --hard + '\n')
proc.stdin.write(git checkout main + '\n')
proc.stdin.write(git pull + '\n')
proc.stdin.write(source webui/bin/activate + '\n')
proc.stdin.write(flask run + '\n')
statusProc = subprocess.run('screen -ls', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

print(statusProc.stdout)
'''if statusProc.stdout == 0:
	print("Success")
	time.sleep(2)
	subprocess.run("exit()")
else:
	print("Something went wrong")
	time.sleep(2)
	subprocess.run("exit()")
# parse screen's output (statusString) for your status list
