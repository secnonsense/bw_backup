# bw_backup
A Bitwarden Unified backup script that uses python and fabric

# Usage:
Replace the hostname/ip address in the "host" variable, and change the NAME placeholder for the docker volume directories for bitwarden and data, and finally choose a path for the scp command to copy your data to.  

This script uses fabric to connection to your bitwarden unified server using SSH keys, runs tar commands to backup the two key directories required to restore your bitwarden installation and then scp's those files locally.  Setup with a cron job on a host to backup these important files.  Also requires SSH key authentication setup between the host where this runs and the bitwarden unified server.


