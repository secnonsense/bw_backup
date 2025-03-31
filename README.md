# bw_backup
A Bitwarden Unified backup script that uses python and fabric

# Usage:
Replace the hostname/ip address in the "host" variable, and change the NAME placeholder for the docker volume directories for bitwarden and data, and finally choose a path for the scp command to copy your data to.  

This script uses fabric to connection to your bitwarden unified server using SSH keys, runs tar commands to backup the two key directories required to restore your bitwarden installation and then scp's those files locally.  Setup with a cron job on a host to backup these important files.  Also requires SSH key authentication setup between the host where this runs and the bitwarden unified server.

After backing up to another server, a verification function is run to confirm the files exists and if so sends a notification via slack webhook (slack webhook url must be saved in a file called .slack in the running users home directory).

Also added backup to s3 bucket, where bucketname variable needs to define the user's s3 bucket, and the user needs to have defined aws tokens in their home directory as used with AWS CLI.  This will backup the files to a folder in the s3 bucket called backup. Webhook notifications will be sent upon backup or failure. Requires boto3 and botocore.exceptions. 


