# SecurityAI
an AI image identification project that is a security system
it can identify dangerous weapons and suspicious people, and then alerting users of danger

![Screenshot 2024-07-18 195525](https://github.com/user-attachments/assets/50807d9c-539a-4d84-b8af-8ceb92f3a7ff)
the AI detecting the position of the body and identifying the knife

## The Algorithm

this code imports the detectNet object identification AI and the poseNet pose identification AI 
these two AI networks are essential to the code

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
display = videoOutput("webrtc://@:8554/output")

These lines of code initialize the AI and the live camera feed

## Running this project

1. Add steps for running this project.
2. Make sure to include any required libraries that need to be installed for your project to run.

[View a video explanation here](video link)
