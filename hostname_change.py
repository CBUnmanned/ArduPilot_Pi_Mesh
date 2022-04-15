# Place on Desktop
# Requires the following line added to rc.local "sudo nano /etc/rc.local"
# python /home/pi/Desktop/hostname_change.py
# 
# Auto runs on start up and sets the hostname of the pi to the MAC Address, allowing access using "000000000000.local", ie MAC Address witout colons
#
# Modified from "https://stackoverflow.com/questions/41582334/how-do-i-change-the-hostname-using-python-on-a-raspberry-pi"

import os

def setHostname(newhostname):
        with open('/etc/hosts', 'r') as file:
                # read a list of lines into data
                data = file.readlines()

        # the host name is on the 6th line following the IP address
        # so this replaces that line with the new hostname
                data[5] = '127.0.1.1       ' + newhostname
                print(data[5])

        # save the file temporarily because /etc/hosts is protected
        with open('temp.txt', 'w') as file:
            file.writelines( data )

        # use sudo command to overwrite the protected file
        os.system('sudo mv temp.txt /etc/hosts')

        # repeat process with other file
        with open('/etc/hostname', 'r') as file:
            data = file.readlines()

        data[0] = newhostname

        with open('temp.txt', 'w') as file:
            file.writelines( data )

        os.system('sudo mv temp.txt /etc/hostname')

#Then call the def
#get current mac address
mac_add = os.popen("cat /sys/class/net/wlan0/address")
# remove semi colons
newHostname = mac_add.read().replace(":", "")

#Get the current hostname
currenthostname = os.popen("hostname")
currenthostname = currenthostname.read()

# if it doesnt match invoke the function to change it
if currenthostname != newHostname:
    print("Changing Hostname to: " + newHostname)
    setHostname(newHostname)
    print("Rebooting to apply name change")
    os.system("sudo reboot -n")
else:
    print("Hostname already set to: " + newHostname)
