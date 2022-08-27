# ArduPilot_Pi_Mesh
BATMAN ADV implemented on Raspberry Pi's to forward MAVLINK

Based off part 1 of this tutorial
https://github.com/binnes/WiFiMeshRaspberryPi/blob/master/part1/PIMESH.md

   
 - You should already have set a Network location to enable wifi on the
   Pi 
 - You should also enable SSH/VNC
 - Legacy Camera should be enabled
 - sudo batctl n should give the MAC address of other nodes

After following part 1 above and verifying the network is setup, copy both files onto the pi desktop and edit rc.local:

    sudo nano /etc/rc.local

Then add the following before the before the BATMAN ADV start script.

    python3 /home/pi/Desktop/hostname_change.py

This will run the python at start up and check if the current hostname is the same as the MAC Address. If it is boot carries on as normal, if not it will set the hostname and then reboot the pi.

To forward mavlink and video MAVProxy and GStreamer need to be installed. 

If you just want MAVProxy, install using:
[Mavproxy Linux](https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html#:~:text=Windows%20installer%20above.-,Linux,-MAVProxy%20runs%20within)

If you want to use SITL to simulate vehicles on nodes use:
[ArduPilot SITL (Inc MavProxy)](https://ardupilot.org/dev/docs/building-setup-linux.html#building-setup-linux)

For Video GStreamer is used, fresh reboot and install

    sudo apt-get install gstreamer1.0-tools


**Usage**
Either plug a pi into an ethernet network for ssh/VNC, or use a screen and keyboard. For the purpose of clarity I will call this the *main* pi, however this is available throughout the mesh.
Running `sudo batctl n` on the *main* pi will list the MAC addresses of the other pis (called *nodes* for clarity) on the network. Given that the hostnames have been changed to the MAC address ssh and VNC work as normal using hostnames rather than an IP address. 

An example network might have this layout:

|  Role| MAC | Hostname|
|--|--|--
|  Main| 00:00:00:00:00 |0000000000.local
|Node 1|11:11:11:11:11 |1111111111.local
|Node 2| 22:22:22:22:22|2222222222.local

Connections can be established using (for node 1):

    ssh pi@1111111111.local

Once logged in

    cd Desktop

Then the streaming can be initialised with Start_AUTOtoUDP_TELEM+Video.py. It takes 3 arguments:

 1. -oH = The mac address (NOT .local!) the data is getting sent to, ie 00:00:00:00:00
 2. -oTP = Telemetry port to use for UDP, normally 14550
 3. -oVP = Video port to use for RTSP, normally 5600

Once running on the node, you should be able to connect on the `main` pi by using either

    mavproxy.py
    or
    mavproxy.py --master=udp:1111111111.local:14550

