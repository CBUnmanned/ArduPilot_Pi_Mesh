# Starts a UDP telemetry and RTSP Video stream. Mavproxy tries to auto connect then forwards onto the hostname given as input arguments. If no camera is detected the video pipeline is closed.

import argparse
import os
import subprocess


parser = argparse.ArgumentParser(description='Start Mavproxy from local device to a specified remote device. Designed to be called via SSH from the GCS/receiving device. example copy/paste: python3 Start_Streaming.py -oH 11:11:11:11:11 -oTP 14550 -oVP 5600')
parser.add_argument('-oH' ,'--outHOSTNAME'     , help='Hostname to send data to. Will auto strip colons from mac addresses', required=True)
parser.add_argument('-oTP','--outtelemetryport', help='Output Port for telemetry (Default 14550)',                           required=True)
parser.add_argument('-oVP','--outvideoport'    , help='Output Port for video (Default 5600)',                                required=True)
args = vars(parser.parse_args())

# Format Hostname to include .local and strip colons if included
args["outHOSTNAME"] = str(args["outHOSTNAME"].replace(":", "")) + ".local"

hostname        = args["outHOSTNAME"]
Telemetryport   = args["outtelemetryport"]
videoport       = args["outvideoport"]

# In Mission Planner set video from:
# udpsrc port=5600 buffer-size=90000 ! application/x-rtp ! rtph264depay ! avdec_h264 ! queue leaky=2 ! videoconvert ! video/x-raw,format=BGRA ! appsink name=outsink sync=false

# Start telemetry stream
bash_Start_Telemetry_Streaming = str("mavproxy.py --out=udpbcast:" + hostname + ":" + Telemetryport) #  + " --non-interactive"
print(bash_Start_Telemetry_Streaming)
#bash_Start_Telemetry_Streaming = os.popen(bash_Start_Telemetry_Streaming, )

# Start Video Stream
bash_Start_video_streaming = str("raspivid -n -w 1280 -h 720 -b 1000000 -fps 15 -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=" + hostname + " port=" + videoport)
print(bash_Start_video_streaming)
#bash_Start_video_streaming = os.popen(bash_Start_video_streaming)


commands = [bash_Start_Telemetry_Streaming, bash_Start_video_streaming]
n = 2 #the number of parallel processes you want
for j in range(max(int(len(commands)/n), 1)):
    procs = [subprocess.Popen(i, shell=True) for i in commands[j*n: min((j+1)*n, len(commands))] ]
    for p in procs:
        p.wait()
        print("done")

while True:
    pass
    #print(bash_Start_Telemetry_Streaming.read())
    #print(bash_Start_video_streaming.read())
