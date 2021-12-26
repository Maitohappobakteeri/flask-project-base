import subprocess

process = subprocess.Popen(
    ['./scripts/db-ip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
DB_IP, err = process.communicate()

AppName = "Flask Base"
ConnectionString = "mysql+mysqlconnector://root:raspberry@" + DB_IP.decode() + "/flasktest" # noqa
Secret = "secretxxxxx"
useCors = True
