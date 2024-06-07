import cv2
import os

# Eğitilmiş yüz tanıma modelini yükle
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_recognition_model.yml")

# Yüz tespiti için OpenCV sınıflandırıcısını yükle
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Test edilecek görüntü dosyasının yolu
test_image_path = "/Users/yigitcanozsahin/Desktop/Fire/faces/usr3/photo_93.jpg"

# Test görüntüsünü yükle
image = cv2.imread(test_image_path)
if image is None:
    print(f"Failed to load image {test_image_path}")
    exit()

# Gri tonlamalı olarak dönüştür
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Yüzleri tespit et
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Tanıma güven eşiği
confidence_threshold = 6010 # Bu değeri deneyerek ayarlayabilirsiniz

# Her tespit edilen yüz için
for (x, y, w, h) in faces:
    # Yüzü dikdörtgenle çerçevele
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Tanınan yüzü bulmak için modeli kullan
    id_, conf = recognizer.predict(gray[y:y+h, x:x+w])

    # Tanıma güven eşiği ile kontrol
    if conf < confidence_threshold:  # Eğer güven değeri eşiğin altındaysa
        cv2.putText(image, f"User {id_}", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
    else:
        cv2.putText(image, "Bilinmeyen", (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

# Sonucu göster
cv2.imshow('Test Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows(),
print(id_)
