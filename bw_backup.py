import fabric
import datetime
import subprocess
import requests
import sys
import json
import os
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

def check_token():
    if os.path.exists(Path.home() / ".slack"):
        with open(Path.home() / ".slack") as f:
            my_variable=f.readlines()[0].strip('\n\r')
            return my_variable
    else:
        print(f"\nThis script requires .slack containing the slack webhook url and it must be stored in {Path.home()}/.slack \n")
        quit()

def webhook(uri,message):
    title = "bwbackup"
    colors={"blue": "#142954","yellow": "#FFFF00","red": "#FF0000", "hotpink": "#FF00FF","green": "#85FF7A"}
    color=colors['yellow']
    body = json.dumps({"pretext": title, "text": message, "color": color})
    try:
        r = requests.post(uri, data=body, headers={"Content-type": "application/json"})
        if r.status_code != 200:
            sys.stderr.write(f"Response code: {r.status_code} {r.text} \n {r.__dict__} \n")
        else:
            print(r.text)
    except Exception as error:
            sys.stderr.write("Exception occurred retrieving data:. Error Code: {}\n".format(error))

def backup_to_s3(target,date,filepath,uri):
    s3 = boto3.resource('s3')
    dest=f"backup/{target}_{date}.tgz"
    bucketname='MYBUCKET'
    try:
        s3.meta.client.upload_file(filepath, bucketname, dest)
        message=f"Filepath '{filepath}' successfully backed up to {bucketname}"
        webhook(uri,message)

    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            message=f"Filepath '{filepath}' does not exist in {bucketname}"
            webhook(uri,message)
        else:
            message=f"Error checking object: {e}"
            webhook(uri,message)

def verify(target,date):
    if os.path.exists(f"/opt/bw_backup/bw_backups/{target}_{date}.tgz"):
        uri=check_token()
        message=f"{target}_{date}.tgz has been successfully backed up!!!"
        webhook(uri,message)
        return uri

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
        filepath=f"/opt/bw_backup/bw_backups/{target}_{date}.tgz"
        subprocess.call([f"scp",f"{host}:/tmp/{target}_{date}.tgz",filepath])
        uri=verify(target,date)
        backup_to_s3(target,date,filepath,uri)

if __name__ == "__main__":
    main() 
