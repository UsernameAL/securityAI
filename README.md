# SecurityAI
an AI image identification project that is a security system
it can identify dangerous weapons and suspicious people, and then alerting users of danger

![Screenshot 2024-07-18 195525](https://github.com/user-attachments/assets/50807d9c-539a-4d84-b8af-8ceb92f3a7ff)

The AI detecting the position of the body and identifying the knife


## Running this project

1. Make sure your Jetson Nano is connected to VSCode and you have camera connected to the nano
2. Make sure you have installed jetson-inference and python3
3. Download the [labels.txt](https://github.com/UsernameAL/securityAI/blob/1877d2d19db1e2ea954d246b00a8070268789326/labels.txt), [securityAI-final.py](https://github.com/UsernameAL/securityAI/blob/c796b82de7005807326167cf8a6a5c0b14508ada/securityAI-final.py), and the [knife-rifledetect.onnx](https://github.com/UsernameAL/securityAI/blob/49a217d03561f9ea55479e8d4c83651b29d8d8f1/knife-rifledetect.onnx) files
4. drag these three downoaded files into a new folder outside of the jetson-inference folder
5. navigate into the new folder containing the files in the terminal using ```cd <folder name>```
6. run the securityAI-final.py using ```python3 securityAI-final.py```
7. to view the output of the live camera, go to ```http://<nano-ip>:8554```


## The Algorithm

The explanation of the code is in the code itself

one special thing is that the suspicion of a person is detected by calculating the ratio of the shoulders and wrists

you can modify this method if you want by using the cordinates from poseNet

the code

```#!/usr/bin/python3

from jetson_inference import detectNet
from jetson_inference import poseNet

from jetson_utils import videoSource, videoOutput

#importing needed things

net = detectNet(
    model="knife-rifledetect.onnx",
    labels="labels.txt",
    input_blob="input_0",
    output_cvg="scores",
    output_bbox="boxes",
    threshold=0.5
)

poseNet = poseNet("resnet18-body", threshold=0.15)
camera = videoSource("v4l2:///dev/video0")
display = videoOutput("webrtc://@:8554/output") # 'my_video.mp4' for file

#initializing AI and camera

while True:
    
    img = camera.Capture()
    
    if img is None: # capture timeout
        continue
    #camera feed
    
    detections = net.Detect(img)
    #detectNet detecting each frame
        
    for x in range(0,len(detections)):
        if(detections[x].ClassID == 1):
            print("Knife detected!")
        elif(detections[x].ClassID == 2):
            print("Rifle detected!")
    #using the feedback from detectNet to print what dangers were detected
    
    poses = poseNet.Process(img)
    #poseNet detecting pose points
    
    for pose in poses:
        # find the keypoint index from the list of detected keypoints
        # you can find these keypoint names in the model's JSON file, 
        # or with net.GetKeypointName() / net.GetNumKeypoints()
        left_wrist_idx = pose.FindKeypoint('left_wrist')
        left_shoulder_idx = pose.FindKeypoint('left_shoulder')
        right_wrist_idx = pose.FindKeypoint('right_wrist')
        right_shoulder_idx = pose.FindKeypoint('right_shoulder')

        # if the keypoint index is < 0, it means it wasn't found in the image
        if left_wrist_idx < 0 or left_shoulder_idx < 0 or right_wrist_idx < 0 or right_shoulder_idx < 0:
            continue
        
        left_wrist = pose.Keypoints[left_wrist_idx]
        left_shoulder = pose.Keypoints[left_shoulder_idx]
        right_wrist = pose.Keypoints[right_wrist_idx]
        right_shoulder = pose.Keypoints[right_shoulder_idx]
        #cordinates of each key position
        
        distance_wrist = (right_wrist.x - left_wrist.x)*(right_wrist.x - left_wrist.x)+(right_wrist.y - left_wrist.y)*(right_wrist.y - left_wrist.y)
        distance_shoulder = (right_shoulder.x - left_shoulder.x)*(right_shoulder.x - left_shoulder.x)+(right_shoulder.y - left_shoulder.y)*(right_shoulder.y - left_shoulder.y)
        #calculating the distance between shoulders and between wrists
        
        if(distance_wrist <= distance_shoulder*0.6):
            print("Suspicious person detected")
        #calculating the ratio of distances, if lower than the ratio, person is counted as suspicious, the ratio is currently 0.6
    
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))```

