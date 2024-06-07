import cv2

# Eğitilmiş yüz tanıma modelini yükle
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_recognition_model.yml")

# Yüz tespiti için OpenCV sınıflandırıcısını yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kamera başlat
cap = cv2.VideoCapture(0)

# Tanıma güven eşiği
confidence_threshold = 100 # Bu değeri deneyerek ayarlayabilirsiniz

while True:
    # Kameradan bir kare yakala
    ret, frame = cap.read()

    # Gri tonlamalı olarak dönüştür
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Her tespit edilen yüz için
    for (x, y, w, h) in faces:
        # Yüzü dikdörtgenle çerçevele
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Tanınan yüzü bulmak için modeli kullan
        id_, conf = recognizer.predict(gray[y:y+h, x:x+w])

        # Tanıma güven eşiği ile kontrol
        if conf < confidence_threshold:  # Eğer güven değeri eşiğin altındaysa
            cv2.putText(frame, f"User {id_}", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Bilinmeyen", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

    # Pencerede kameradan alınan görüntüyü göster
    cv2.imshow('frame', frame)

    # Çıkmak için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera kapat
cap.release()
cv2.destroyAllWindows()
