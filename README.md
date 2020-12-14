# EyeBlinkDetection
Senior Project
The main purpose of this study is to retrieve data by counting eye-blinks. The input of the project is the user’s eyes, which are read from the camera sensor. The blinks are counted in process at a certain time.
The input stage of the project, which will be designed as stand-alone, detects the user's face and eyes from the video image from the 5 MP camera. In the process stage, it is decided to use Raspberry Pi 3B + and Python language. The project continued with face and eye detection from the live video. Facial Landmarks approach is used. Whether the user blinked was calculated using the EAR. In output stage, the beginning of the 10 second period is shown to the patient. The patient will express herself/himself comfortably and will see the correct message on the LCD.
By completing the source analysis, it was agreed to use the formulation The Eye Aspect Ratio (EAR).This ratio is obtained from Soukupová and Čech’s Real-Time Eye Blink Detection Using Facial Landmarks article as an idea. Thus, the desired rate was obtained without rounding and loss of data.

