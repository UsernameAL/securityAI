#!/usr/bin/python3

from jetson_inference import detectNet

from jetson_utils import videoSource, videoOutput

net = detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = videoSource("v4l2:///dev/video0")
display = videoOutput("webrtc://@:8554/output") # 'my_video.mp4' for file
danger = False

while True:
    img = camera.Capture()
    
    if img is None: # capture timeout
        continue
    
    detections = net.Detect(img)
    
    if(danger):
        print("Danger Detected!")
    
    for x in range(0,len(detections)):
        #print("hello" + str(detections[x].ClassID))
        if(detections[x].ClassID==49):
            danger = True
    
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))