import fabric
import datetime
import subprocess

def run_command(host,command):
    result=fabric.Connection(host).run(command)
    print(result)


def main():
    host="1.1.1.1"
    path="/var/lib/docker/volumes/"
    date=datetime.datetime.utcnow().strftime("%m%d%Y")
    targets=["NAME_bitwarden","NAME_data"]
    for target in targets:
        command=f"sudo tar zcvf /tmp/{target}_{date}.tgz {path}{target}/"
        run_command(host,command)
        subprocess.call([f"scp",f"{host}:/tmp/{target}_{date}.tgz",f"/PATH/{target}_{date}.tgz"])

if __name__ == "__main__":
    main() 
