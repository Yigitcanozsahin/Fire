import cv2
import os
import numpy as np
from PIL import Image  # Pillow kütüphanesinden Image sınıfını içe aktar

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Yüz veri setini yükleyin
def load_faces(directory):
    faces = []
    labels = []
    label_ids = {}  # label_ids adlı bir sözlük tanımlayın

    label_id = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                label = os.path.basename(root).replace(" ", "-").lower()
                if not label in label_ids:
                    label_ids[label] = label_id
                    label_id += 1
                id_ = label_ids[label]
                pil_image = Image.open(path).convert("L")  # Gri tonlamada yükleme
                image_array = np.array(pil_image, "uint8")
                faces.append(image_array)
                labels.append(id_)
    return faces, labels

# Yüz tanıma modelini eğitin
def train_faces(faces, labels):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    return recognizer

# Kamera başlat
cap = cv2.VideoCapture(0)

# Tanımlanan yüzleri yükle
faces, labels = load_faces("dataset")

# Yüz tanıma modelini eğitin
recognizer = train_faces(faces, labels)

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()
    
    # Kareyi griye dönüştür
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Yüzleri tanı
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # Tanıma yap
        id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        
        # Tanıma sonucunu ekrana yazdır
        if confidence < 100:
            name = "Yüz " + str(id_)
            cv2.putText(frame, name, (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Gösterilen kareyi ekrana yansıt
    cv2.imshow('Frame', frame)
    
    # Çıkış için 'q' tuşuna basıldığında döngüyü kır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()
