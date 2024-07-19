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

[View a video explanation here](video link)



## The Algorithm

The explanation of the code is in the code itself

one special thing is that the suspicion of a person is detected by calculating the ratio of the shoulders and wrists

you can modify this method if you want by using the cordinates from poseNet

