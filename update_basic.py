import subprocess

subprocess.run("deactivate", shell=True)
subprocess.run(["git reset", "--hard"], shell=True)
subprocess.run(["git checkout", "main"], shell=True)
subprocess.run("git pull", shell=True)
subprocess.run(["source", "webui/bin/activate"], shell=True)
subprocess.run("flask run", shell=True)
