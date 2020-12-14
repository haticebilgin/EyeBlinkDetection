# ikinci deneme kodu
# =============================================================================
# coding=utf-8
import cv2  # open cv kutuphanesi
import dlib
import time
from math import hypot
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
from serial import Serial
import serial
import struct
import RPi.GPIO as GPIO


GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)
font = cv2.FONT_HERSHEY_TRIPLEX

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
loop = 0

while loop < 15 :
    focus = 0
    total = 0
    count = 0

    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 60
    rawCapture = PiRGBArray(camera, size=(320, 240))
    camera.brightness = 50
    begin = time.time()

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        end = time.time()
        if end - begin > 10:  # periyodun sifirlandigi yer. her goz kirpma aktivitesi 10 sn surer.
            break
        #_, frame = camera.read()  # capture.read iki deger donduruyor.ilk deger onemsiz oldugu icin alt tire koyduk
        image = frame.array
        #frame = imutils.resize(frame, width=450)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) de olabilir denemek lazim
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)  # bulunan tum yuzler bu arrayda
        for face in faces:
            landmarks = predictor(gray, face)
            # =============================================================================
            # LEFT EYE
            point_36 = (landmarks.part(36).x, landmarks.part(36).y)
            point_39 = (landmarks.part(39).x, landmarks.part(39).y)
            point_37 = (landmarks.part(37).x, landmarks.part(37).y)
            point_38 = (landmarks.part(38).x, landmarks.part(38).y)
            point_41 = (landmarks.part(41).x, landmarks.part(41).y)
            point_40 = (landmarks.part(40).x, landmarks.part(40).y)

            # =============================================================================

            a = hypot((point_37[0] - point_41[0]), (point_37[1] - point_41[1]))
            b = hypot((point_38[0] - point_40[0]), (point_38[1] - point_40[1]))
            c = hypot((point_36[0] - point_39[0]), (point_36[1] - point_39[1]))
            ear_1= (a+b)/(2*c)
            # =============================================================================
            # RIGHT EYE
            point_42 = (landmarks.part(42).x, landmarks.part(42).y)
            point_43 = (landmarks.part(43).x, landmarks.part(43).y)
            point_44 = (landmarks.part(44).x, landmarks.part(44).y)
            point_45 = (landmarks.part(45).x, landmarks.part(45).y)
            point_46 = (landmarks.part(46).x, landmarks.part(46).y)
            point_47 = (landmarks.part(47).x, landmarks.part(47).y)
            # =============================================================================

            d = hypot((point_43[0] - point_47[0]), (point_43[1] - point_47[1]))
            e = hypot((point_44[0] - point_46[0]), (point_44[1] - point_46[1]))
            f = hypot((point_42[0] - point_45[0]), (point_42[1] - point_45[1]))
            ear_2 = (d + e) / (2 * f)
            #eye aspect of ratio
            # ratio ve LCD
            ear = (ear_1 + ear_2) / 2
            #if ear < 0.34 or ear_1<0.34 or ear_2<0.34 :
            if ear < 0.34:  #goz kapali
                count += 1

            else:  #goz acik
                if count >= 3:
                    total += 1
                    # cv2.putText(frame, "goz kirpti", (50, 150), font, 1, (0, 0, 255))

                count = 0
            cv2.putText(image, "Blinks: {}".format(total), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # =============================================================================
            #if (focus==0):
             #   time.sleep(2)
               # focus=focus+1
        #cv2.imshow("Face Detection", image)
        key = cv2.waitKey(50) & 0xff
        rawCapture.truncate(0)

    camera.stop_preview()
    camera.close()
    #camera.release()
    # =============================================================================

    port=Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.0)
    print(port)
    time.sleep(1)
    i=0
    k=struct.pack('B', 0xff)

    while True:
        if total==0:
            print("Hic kirpmadin")
        elif total == 1:
            print("1 kez kirptin, Yardim")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Yardim".encode())
            port.write('"'.encode())
        elif total == 2:
            print("2 kez kirptin, Ilac vakti")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Ilac".encode())
            port.write('"'.encode())
        elif total == 3:
            print("3 kez kirptin, Sag kolum")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Sag kolum".encode())
            port.write('"'.encode())
        elif total == 4:
            print("4 kez kirptin, Sol kolum")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Sol kolum".encode())
            port.write('"'.encode())
        elif total == 5:
            print("5 kez kirptin, Basim")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Basim".encode())
            port.write('"'.encode())
        elif total == 6:
            print("6 kez kirptin, Sol bacak")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Sol bacak".encode())
            port.write('"'.encode())
        elif total == 7:
            print("7 kez kirptin, Sag bacak")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Sag bacak".encode())
            port.write('"'.encode())
        elif total == 8:
            print("8 kez kirptin, Hava almaliyim")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Hava almaliyim".encode())
            port.write('"'.encode())
        elif total == 9:
            print("9 kez kirptin, Mide")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Mide".encode())
            port.write('"'.encode())
        elif total == 10:
            print("10 kez kirptin")
            port.write(b"t0.txt=")
            port.write('"'.encode())
            port.write("Aciktim".encode())
            port.write('"'.encode())
        else:
            print("10'dan fazla kirptin, {} kez kirptin".format(total))

        port.write(k)
        port.write(k)
        port.write(k)
        time.sleep(1)
        i = i + 1
        if(i==2):
            break
    loop=loop+1
    time.sleep(2)

GPIO.output(12, GPIO.LOW)
cv2.destroyAllWindows()
