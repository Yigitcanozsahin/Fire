import cv2
import os

# Yüz tanıma için ön eğitilmiş modeli yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kullanıcı veritabanı
users = {"person1": "1234", "person2": "5678"}

# Kamerayı aç
cap = cv2.VideoCapture(0)

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()

    # Kareyi griye dönüştür
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri algıla
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Algılanan yüzlerin etrafına dikdörtgen çiz
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Yüz bölgesini gri tonlama ve boyutlandırma
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Yüz tanıma ve kimlik doğrulama
        for user, password in users.items():
            # Yüzünüzü tanıma ve doğrulama işlemlerini buraya ekleyin
            pass

    # Pencereye kareyi ve algılanan yüzleri göster
    cv2.imshow('Face ID', frame)

    # Çıkmak için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Pencereyi kapat ve kamerayı serbest bırak
cap.release()
cv2.destroyAllWindows()
