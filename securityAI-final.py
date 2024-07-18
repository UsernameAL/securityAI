#!/usr/bin/python3

from jetson_inference import detectNet
from jetson_inference import poseNet

from jetson_utils import videoSource, videoOutput

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
danger = False

while True:
    
    img = camera.Capture()
    
    if img is None: # capture timeout
        continue
    
    detections = net.Detect(img)
        
    for x in range(0,len(detections)):
        if(detections[x].ClassID == 1):
            print("Knife detected!")
        elif(detections[x].ClassID == 2):
            print("Rifle detected!")
    
    poses = poseNet.Process(img)

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
        
        distance_wrist = (right_wrist.x - left_wrist.x)*(right_wrist.x - left_wrist.x)+(right_wrist.y - left_wrist.y)*(right_wrist.y - left_wrist.y)
        distance_shoulder = (right_shoulder.x - left_shoulder.x)*(right_shoulder.x - left_shoulder.x)+(right_shoulder.y - left_shoulder.y)*(right_shoulder.y - left_shoulder.y)
        
        if(distance_wrist <= distance_shoulder*0.6):
            print("Suspicious person detected")
    
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))