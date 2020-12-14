# =============================================================================
import cv2  # open cv kutuphanesi
import dlib
import time
from math import hypot
import imutils

font = cv2.FONT_HERSHEY_TRIPLEX
cap = cv2.VideoCapture(0)  # primary kamerayı bulduk
detector = dlib.get_frontal_face_detector()  # yüz algılama
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

begin = time.time()
focus=0
total=0
count = 0

while (True):
    end = time.time()
    if end - begin > 10:  # periyodun sifirlandigi yer. her goz kirpma aktivitesi 10 sn surer.
        break
    _, frame = cap.read()  # capture.read iki deger donduruyor.ilk deger onemsiz oldugu icin alt tire koyduk
    frame = imutils.resize(frame, width=450) #cozunurluk degıstırdık
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # resim griye çevrildi.
    # gri frame daha aydınlık oldugu ıcın renkli göruntu grıye cekıldı
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
        # aradaki uzaklıgı bulmak :
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
        # aradaki uzaklıgı bulmak :
        d = hypot((point_43[0] - point_47[0]), (point_43[1] - point_47[1]))
        e = hypot((point_44[0] - point_46[0]), (point_44[1] - point_46[1]))
        f = hypot((point_42[0] - point_45[0]), (point_42[1] - point_45[1]))
        ear_2 = (d + e) / (2 * f)

        # ratio
        ear = (ear_1 + ear_2) / 2

        if ear < 0.30:  #goz kapatmis olabilir
            count += 1

        elif count >= 3:
            total += 1
            count = 0

        cv2.putText(frame, "Blinks: {}".format(total), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # =============================================================================

    cv2.imshow("Face Detection", frame)
    key = cv2.waitKey(50) & 0xff

# =============================================================================
if total==0:
    print("Hic kirpmadin")
elif total == 1:
    print("Yardım eder misin")
elif total == 2:
    print("Ilac vaktim geldi")
elif total == 3:
    print("Sag Kolum Agriyor")
elif total == 4:
    print("Sol Kolum Agriyor")
elif total == 5:
    print("Basim Agriyor")
elif total == 6:
    print("Sol Bacagim Agriyor")
elif total == 7:
    print("Sag Bacagim Agriyor")
elif total == 8:
    print("Hava almaliyim")
elif total == 9:
    print("Midem Agriyor")
elif total == 10:
    print("Aciktim")
else:
    print("10'dan fazla kirptin, {} kez kırptın".format(total))


cap.release()
cv2.destroyAllWindows()
