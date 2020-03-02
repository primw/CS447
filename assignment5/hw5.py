#!/usr/bin/env python3
import subprocess as sp    #Can execute applications
import argparse            #Used for parsing arguments
import logging             #Sets up logging
import sys

##### LOGGING SETUP #####
logger = logging.getLogger()
logger.setLevel(logging.INFO)           #Create Log

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)                                              
stdoutFormat = logging.Formatter('%(asctime)s,%(levelname)s, %(name)s, %(funcName), %(message)s')
handler.setFormatter(stdoutFormat)                             

logger.addHandler(handler)              #Add Handler to Log - logs to file + stdout
#########################


#Use argparse to add required command line arguments
parser = argparse.ArgumentParser(description='Python script that creats a mdraid RAID device from three loop devices.')
parser.add_argument('filename1', type=str, help='End file names with .img')
parser.add_argument('filename2', type=str)
parser.add_argument('filename3', type=str)


#Assigns each command line argument to a variable
args = parser.parse_args()
filenames = [args.filename1, args.filename2, args.filename3]
loopdevs = []
partSize = 4.5
index = 0

#For each file: create, losetup, and partition
for filename in filenames:
    sp.Popen(['truncate', '-s', '5G', filename])
    losetup = sp.Popen(['losetup', '-f', '--show', filename], stdout=sp.PIPE)
    output, err  = losetup.communicate()
    output = output.decode('utf-8').strip('\n')
    loopdevs.append(output)

    sp.Popen(['parted', '-s', f'{loopdevs[index]}', "'mklabel", 'gpt', 'mkpart', 'lvpart1', '1M', f"{partSize}G'"])
    index += 1


#Create a raid1 using two partitions and using one as a spare
sp.Popen(['mdadm', '-C', '/dev/md0', '-l', 'raid1', '-n', '2', loopdevs[0], loopdevs[1]])
sp.Popen(['mdadm', '--add-spare', '/dev/md0', loopdevs[2]])


#Create Physical Volumes for each loop device
for loopdev in loopdevs:
    sp.Popen(['pvcreate', loopdev])

#Create a Volume Group for all the loop devices
sp.Popen(['vgcreate', 'vg0', loopdevs[0], loopdevs[1], loopdevs[2]])
lvNames = ["lv0", "lv1"]

for lv in lvNames:
    sp.Popen(['lvcreate', '-L', '1G', '-n',  lv, 'vg0'])



        


